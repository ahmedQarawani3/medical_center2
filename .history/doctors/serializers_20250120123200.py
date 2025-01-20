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
from rest_framework import serializers
from .models import Doctor, Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']


class DoctorSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True, write_only=True)  # مواعيد التوافر للكتابة فقط

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'availabilities']

    def create(self, validated_data):
        availabilities_data = validated_data.pop('availabilities')  # استخراج مواعيد التوافر
        doctor = Doctor.objects.create(**validated_data)  # إنشاء الطبيب
        for availability in availabilities_data:
            Availability.objects.create(doctor=doctor, **availability)  # إضافة المواعيد
        return doctor

