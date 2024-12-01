# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time_slot', 'status']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time_slot']

    def validate(self, data):
        """
        التحقق إذا كان الموعد محجوزًا مسبقًا
        """
        if Appointment.objects.filter(doctor=data['doctor'], date=data['date'], time_slot=data['time_slot'], status='booked').exists():
            raise serializers.ValidationError("This appointment is already booked.")
        return data
