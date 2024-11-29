from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from datetime import datetime

@api_view(['GET'])
def list_appointments(request):
    """
    قائمة المواعيد المتاحة
    """
    appointments = Appointment.objects.filter(status='available')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_appointment(request):
    """
    حجز موعد للمريض
    """
    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    
    if serializer.is_valid():
        # استخدام filter بدلاً من get لتجنب الأخطاء
        appointment = Appointment.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot'],
            status='available'
        ).first()
        
        if not appointment:
            return Response({"error": "This appointment slot is not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # حجز الموعد للمريض
        appointment.patient = request.user.patient
        appointment.status = 'booked'
        appointment.save()
        return Response({"message": "Appointment booked successfully."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reschedule_appointment(request, appointment_id):
    """
    إعادة جدولة الموعد
    """
    try:
        # التحقق من وجود الموعد
        appointment = Appointment.objects.get(id=appointment_id, patient=request.user.patient)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # التحقق من إمكانية التعديل على الموعد
    if not appointment.can_cancel_or_reschedule():
        return Response({"error": "Cannot reschedule less than 8 hours before the appointment."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    
    if serializer.is_valid():
        # إلغاء الموعد القديم
        appointment.status = 'available'
        appointment.patient = None
        appointment.save()

        # حجز الموعد الجديد
        new_appointment = Appointment.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot'],
            status='available'
        ).first()
        
        if not new_appointment:
            return Response({"error": "New appointment slot is not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        new_appointment.patient = request.user.patient
        new_appointment.status = 'booked'
        new_appointment.save()
        return Response({"message": "Appointment rescheduled successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
