from rest_framework import serializers
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from billing.models import Payment


# 1. Serializer لـ Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor  # يفترض أن قسم الـ Doctor يحتوي على معلومات القسم
        fields = ['id', 'name', 'description']


# 2. Serializer لـ Doctor
class DoctorSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'department']


# 3. Serializer لـ Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # إضافة قيمة المعاينة

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time', 'status', 'consultation_fee']
