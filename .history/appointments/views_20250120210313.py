
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
from django.utils.dateparse import parse_datetime

class BookAppointmentView(APIView):
    def post(self, request):
        data = request.data
        doctor_id = data.get("doctor_id")
        appointment_time = data.get("appointment_time")  # يجب أن يكون بصيغة ISO-8601

        # التأكد من وجود الطبيب
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

        # التحقق من صحة الوقت
        appointment_time = parse_datetime(appointment_time)
        if not appointment_time:
            return Response({"error": "Invalid appointment time."}, status=status.HTTP_400_BAD_REQUEST)

        # البحث عن التوفر
        availability = Availability.objects.filter(
            doctor=doctor,
            day=appointment_time.strftime("%A"),
            start_time__lte=appointment_time.time(),
            end_time__gte=appointment_time.time()
        ).first()

        if not availability:
            return Response({"error": "Selected appointment slot is not available."}, status=status.HTTP_400_BAD_REQUEST)

        # التحقق من أن الموعد غير محجوز
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_time=appointment_time
        ).exists():
            return Response({"error": "Appointment slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء الموعد
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            appointment_time=appointment_time
        )

        return Response({"message": "Appointment booked successfully.", "appointment_id": appointment.id}, status=status.HTTP_201_CREATED)



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

