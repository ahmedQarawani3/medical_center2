
from .models import Patient, Notification
from rest_framework import serializers
from rest_framework import serializers
from rest_framework import serializers

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Patient  
        fields = ['user', 'name', 'address', 'phone_number', 'date_of_birth', 'gender', 'height', 'weight']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'patient', 'notification_type', 'message', 'notification_date', 'created_at', 'read']




class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'name', 'address', 'date_of_birth', 'gender', 
            'height', 'weight', 'profile_picture',
            'medical_history', 'allergies', 'past_surgeries' 
        ]  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

