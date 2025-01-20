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
    availabilities = AvailabilitySerializer(many=True, write_only=True)  # كتابة فقط لتجنب الأخطاء في التحقق

    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'availabilities']

    def create(self, validated_data):
        # استخراج المواعيد من البيانات التي تم التحقق منها
        availabilities_data = validated_data.pop('availabilities', [])
        doctor = Doctor.objects.create(**validated_data)

        # إنشاء مواعيد التوافر المرتبطة بالطبيب
        for availability in availabilities_data:
            Availability.objects.create(doctor=doctor, **availability)

        return doctor


