
# views.py
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Patient, Notification
from .serializers import PatientSerializer, NotificationSerializer
from appointments.models import Appointment
from medical.models import Medication

@api_view(['GET'])
def patient_details(request, name):
    try:
        patients = Patient.objects.filter(name=name)
        if not patients.exists():
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def patient_notifications(request, patient_id):
    try:
        notifications = Notification.objects.filter(patient__user_id=patient_id).order_by('-notification_date')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_appointment_notification(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        patient = appointment.patient

        notification_time = appointment.date - timedelta(days=1)
        message = f"Reminder: You have an appointment with Dr. {appointment.doctor.name} on {appointment.date}."

        notification = Notification.objects.create(
            patient=patient,
            notification_type='appointment',
            message=message,
            notification_date=notification_time,
        )

        return Response({"message": "Notification created."}, status=status.HTTP_201_CREATED)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_medication_notification(request, medication_id):
    try:
        medication = Medication.objects.get(id=medication_id)
        patient = medication.patient

        notification_time = timezone.now()
        message = f"Reminder: It's time to take your medication {medication.name}."

        notification = Notification.objects.create(
            patient=patient,
            notification_type='medication',
            message=message,
            notification_date=notification_time,
        )
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Medication.DoesNotExist:
        return Response({"error": "Medication not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_notifications(request):
    try:
        patient = request.user
        notifications = Notification.objects.filter(patient=patient).order_by('-notification_date')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return Response({"message": "Notification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.message = request.data.get('message', notification.message)
        notification.notification_type = request.data.get('notification_type', notification.notification_type)
        notification.save()
        return Response({"message": "Notification updated successfully"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
