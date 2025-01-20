from rest_framework import serializers
from .models import Doctor, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

# doctors/serializers.py
from rest_framework import serializers
from .models import Doctor
from .models import Doctor, Availability


from rest_framework import serializers
from .models import Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']
class DoctorSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True)  # لتضمين مواعيد التوافر للطبيب

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'availabilities']