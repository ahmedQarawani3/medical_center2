# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.contrib.auth import get_user_model

# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model


# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'password','role']

    def create(self, validated_data):
        # هنا نقوم بإنشاء المستخدم مع رقم الهاتف كـ username
        user = get_user_model().objects.create_user(
            username=validated_data['phone_number'],  # استخدام رقم الهاتف كـ username
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user