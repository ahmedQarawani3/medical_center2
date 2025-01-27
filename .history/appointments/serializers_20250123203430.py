from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time_slot', 'status']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot']

    def validate(self, data):
        # تحقق من أن الموعد غير محجوز
        if Appointment.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            time_slot=data['time_slot'],
            status='booked'
        ).exists():
            raise serializers.ValidationError("This appointment slot is already booked.")
        # تحقق من أن التاريخ والوقت ليس في الماضي
        from datetime import datetime
        if data['date'] < datetime.now().date():
            raise serializers.ValidationError("Cannot book an appointment in the past.")
        return data
