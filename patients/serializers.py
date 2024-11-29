from rest_framework import serializers
from .models import Patient
from .models import Notification
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'patient', 'notification_type', 'message', 'notification_date', 'created_at']

