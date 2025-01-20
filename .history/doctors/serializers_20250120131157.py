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

from rest_framework import serializers
from .models import Doctor, Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']

class DoctorSerializer(serializers.ModelSerializer):
    # يتم تضمين مواعيد الطبيب داخل الحقل `availabilities`
    availabilities = AvailabilitySerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'years_of_experience', 'consultation_fee', 'department', 'user', 'availabilities']

    def to_representation(self, instance):
        # هنا نعرض معلومات الطبيب أولاً، ثم المواعيد تحتها
        representation = super().to_representation(instance)
        availabilities = representation['availabilities']
        
        # ترتيب المواعيد حسب اليوم ثم الوقت
        days_order = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }

        availabilities.sort(key=lambda x: (days_order[x['day']], x['start_time']))

        # بعد ترتيب المواعيد، نعرضها تحت معلومات الطبيب
        representation['availabilities'] = availabilities
        return representation






