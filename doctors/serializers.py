from rest_framework import serializers
from .models import Doctor, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'department', 'biography']
