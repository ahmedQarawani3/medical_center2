from rest_framework import serializers
from .models import Doctor, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class DoctorSerializer(serializers.ModelSerializer):
    department = serializers.CharField()  # بدلاً من `DepartmentSerializer`

    class Meta:
        model = Doctor
        fields = ['user', 'department', 'specialization', 'years_of_experience', 'is_active']
