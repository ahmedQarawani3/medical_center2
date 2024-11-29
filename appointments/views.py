from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from datetime import datetime

@api_view(['GET'])
def list_appointments(request):
    appointments = Appointment.objects.filter(status='available')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_appointment(request):
    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    if serializer.is_valid():
        appointment = Appointment.objects.get(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot'],
            status='available'
        )
        appointment.patient = request.user.patient
        appointment.status = 'booked'
        appointment.save()
        return Response({"message": "Appointment booked successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reschedule_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id, patient=request.user.patient)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if not appointment.can_cancel_or_reschedule():
        return Response({"error": "Cannot reschedule less than 8 hours before the appointment."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    serializer = AppointmentCreateSerializer(data=data)
    if serializer.is_valid():
        appointment.status = 'available'
        appointment.patient = None
        appointment.save()

        new_appointment = Appointment.objects.get(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot'],
            status='available'
        )
        new_appointment.patient = request.user.patient
        new_appointment.status = 'booked'
        new_appointment.save()
        return Response({"message": "Appointment rescheduled successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
