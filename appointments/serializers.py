from rest_framework import serializers
from .models import Appointment
from billing.models import Payment  # استيراد Payment من billing.models

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time_slot', 'status']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time_slot', 'payment']

    def validate(self, data):
        if Appointment.objects.filter(doctor=data['doctor'], date=data['date'], time_slot=data['time_slot'], status='booked').exists():
            raise serializers.ValidationError("This appointment slot is already booked.")
        return data
