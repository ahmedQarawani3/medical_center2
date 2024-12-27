
# serializers.py
from rest_framework import serializers
from .models import Patient, Notification

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = ['user', 'name', 'address', 'phone_number', 'date_of_birth', 'gender', 'height', 'weight']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'patient', 'notification_type', 'message', 'notification_date', 'created_at', 'read']
