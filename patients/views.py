from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Notification
from .serializers import PatientSerializer, NotificationSerializer
from appointments.models import Appointment
from medical.models import Medication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import PatientProfileSerializer
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class CreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]  # تأكد من أن المستخدم مسجل دخول

    def post(self, request):
        # التحقق من أن المستخدم هو المسؤول (Admin)
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to create notifications."}, status=status.HTTP_403_FORBIDDEN)
        
        # متابعة تنفيذ الكود لإنشاء الإشعار إذا كانت الصلاحية صحيحة
        title = request.data.get("title")
        message = request.data.get("message")
        expiry_date = request.data.get("expiry_date")
        
        if not title or not message or not expiry_date:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification.objects.create(
            title=title,
            message=message,
            expiry_date=expiry_date,
        )

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class ListNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.active().order_by('-created_at')  # جلب فقط الإشعارات النشطة
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class UpdatePatientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        try:
            patient = request.user.patient  
        except Patient.DoesNotExist:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientProfileSerializer(patient)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            patient = request.user.patient  
        except Patient.DoesNotExist:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientProfileSerializer(patient, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
