from rest_framework import serializers
from .models import Doctor, Department
from .models import Doctor, Availability

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']






class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']

class DoctorSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'user', 'availabilities']





