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
    availabilities = AvailabilitySerializer(many=True, write_only=True)

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'user', 'availabilities']

    def create(self, validated_data):
        availabilities_data = validated_data.pop('availabilities', [])
        user = validated_data.pop('user')  # الحصول على المستخدم
        doctor = Doctor.objects.create(user=user, **validated_data)  # إنشاء الطبيب وربطه بالمستخدم

        for availability in availabilities_data:
            Availability.objects.create(doctor=doctor, **availability)

        return doctor



