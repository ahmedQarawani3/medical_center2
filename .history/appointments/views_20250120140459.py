
from billing.models import Payment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser 
from .models import Appointment
from doctors.models import Doctor
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments(request):
    """عرض المواعيد المتاحة"""
    appointments = Appointment.objects.filter(status='available')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# appointments/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from billing.models import Payment
from appointments.models import Appointment

@api_view(['POST'])
def book_appointment(request):
    """حجز موعد جديد"""
    doctor_id = request.data.get('doctor_id')
    date = request.data.get('date')
    time_slot = request.data.get('time_slot')
    payment_transaction_id = request.data.get('payment_transaction_id')  # استخدام payment_transaction_id

    # تحقق من وجود موعد متاح
    try:
        appointment = Appointment.objects.get(
            doctor_id=doctor_id,
            date=date,
            time_slot=time_slot,
            status='available'
        )
    except Appointment.DoesNotExist:
        return Response({"error": "Selected appointment slot is not available."}, status=status.HTTP_404_NOT_FOUND)

    # تحقق من الدفع
    if not payment_transaction_id:
        return Response({"error": "Payment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.get(transaction_id=payment_transaction_id)
        if payment.status != 'paid':
            return Response({"error": "Payment must be completed before booking the appointment."}, status=status.HTTP_400_BAD_REQUEST)
    except Payment.DoesNotExist:
        return Response({"error": "Invalid payment."}, status=status.HTTP_404_NOT_FOUND)

    # حجز الموعد
    appointment.status = 'booked'
    appointment.patient = request.user.patient
    appointment.payment_transaction_id = payment_transaction_id  # تخزين payment_transaction_id
    appointment.save()

    return Response({"message": "Appointment booked successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reschedule_appointment(request, appointment_id):
    """إعادة جدولة موعد (فقط للإدارة)"""
    # التأكد من أن المستخدم هو الإدارة فقط
    if not request.user.is_staff:  # تحقق إذا كان المستخدم هو موظف المركز
        return Response({"error": "Only admin can reschedule appointments."}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    # التحقق من إمكانية إعادة الجدولة (مثل التحقق من الوقت المتبقي)
    if appointment.date - datetime.now().date() < timedelta(hours=8):
        return Response({"error": "Cannot reschedule less than 8 hours before the appointment."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    if serializer.is_valid():
        try:
            # التحقق من أن الفتحة الزمنية الجديدة متاحة
            new_appointment = Appointment.objects.get(
                doctor=data['doctor'],
                date=data['date'],
                time_slot=data['time_slot'],
                status='available'
            )
        except Appointment.DoesNotExist:
            return Response({"error": "New appointment slot is not available."}, status=status.HTTP_404_NOT_FOUND)

        # إعادة الموعد الحالي إلى الحالة المتاحة
        appointment.status = 'available'
        appointment.patient = None
        appointment.save()

        # حجز الموعد الجديد
        new_appointment.patient = appointment.patient  # نقل المريض إلى الموعد الجديد
        new_appointment.status = 'booked'
        new_appointment.save()

        return Response({"message": "Appointment rescheduled successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def doctor_availability(request, doctor_id):
    """عرض الأوقات المتاحة للطبيب"""
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        appointments = Appointment.objects.filter(doctor=doctor)
        booked_slots = appointments.filter(status='booked').values_list('time_slot', flat=True)
        
        available_times = [
            time for time in doctor.available_times if time not in booked_slots
        ]

        return Response({
            "doctor": doctor.name,
            "available_times": available_times,
            "booked_slots": list(booked_slots),
        })
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

