from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_appointments(request):
    """عرض المواعيد المتاحة"""
    appointments = Appointment.objects.filter(status='available')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    """حجز موعد جديد"""
    if not hasattr(request.user, 'patient'):
        return Response({"error": "Only patients can book appointments."}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    if serializer.is_valid():
        try:
            appointment = Appointment.objects.get(
                doctor=data['doctor'],
                date=data['date'],
                time_slot=data['time_slot'],
                status='available'
            )
        except Appointment.DoesNotExist:
            return Response({"error": "Selected appointment slot is not available."}, status=status.HTTP_404_NOT_FOUND)

        appointment.patient = request.user.patient
        appointment.status = 'booked'
        appointment.save()
        return Response({"message": "Appointment booked successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from datetime import datetime, timedelta
from rest_framework.permissions import IsAdminUser  # استيراد صلاحية الإدارة

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
