from accounts.utils import send_sms
from patients.models import Patient
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
import random

@api_view(['POST'])
def register_patient(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name')
    role = 'patient'

    if not phone_number or not password or not name:
        return Response({"detail": "All fields (phone_number, password, name) are required."}, status=status.HTTP_400_BAD_REQUEST)

    if get_user_model().objects.filter(phone_number=phone_number).exists():
        return Response({"detail": "Phone number is already registered. Please use another phone number."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_user_model().objects.create_user(
            username=phone_number,
            phone_number=phone_number,
            password=password,
            role=role
        )
        # توليد كود التفعيل
        verification_code = str(random.randint(1000, 9999))
        send_sms(phone_number, f"Your verification code is: {verification_code}")

        # تخزين الكود مؤقتًا باستخدام cache
        cache.set(phone_number, verification_code, timeout=300)  # الكود صالح لمدة 5 دقائق

        # إنشاء ملف تعريف المريض
        Patient.objects.create(user=user, name=name)

        return Response({"detail": "Patient registered successfully. Please confirm your account."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_registration(request):
    phone_number = request.data.get('phone_number')
    code = request.data.get('verification_code')

    if not phone_number or not code:
        return Response({"detail": "Phone number and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من الكود المخزن في cache
    cached_code = cache.get(phone_number)
    if cached_code is None or cached_code != code:
        return Response({"detail": "Invalid phone number or code."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # العثور على المستخدم وتفعيل الحساب
        user = get_user_model().objects.get(phone_number=phone_number)
        user.is_active = True
        user.save()

        # إزالة الكود من cache بعد التحقق
        cache.delete(phone_number)

        return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
    except get_user_model().DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)









@api_view(['POST'])
def login_user(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    role = request.data.get("role")

    if not phone_number or not password or not role:
        return Response({"detail": "Phone number, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

    # البحث عن المستخدم باستخدام الرقم الهاتفي
    try:
        user = get_user_model().objects.get(phone_number=phone_number)
    except get_user_model().DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # التحقق من كلمة المرور
    if not user.check_password(password):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # التحقق من الدور
    if user.role != role:
        return Response({"detail": "Role mismatch. Expected role is '{}', got '{}'.".format(user.role, role)}, status=status.HTTP_400_BAD_REQUEST)

    # إنشاء رموز التوثيق
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role  # تضمين الدور في التوكن
    access_token = str(refresh.access_token)

    return Response({
        "access": access_token,
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)






@api_view(['POST'])
def logout_user(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def reset_password(request):
    phone_number = request.data.get("phone_number")

    try:
        user = get_user_model().objects.get(phone_number=phone_number)
        new_password = str(random.randint(100000, 999999))  # Generate a new password
        user.set_password(new_password)
        user.save()

        send_sms(phone_number, f"كلمه السر الجديدة لديك هي: {new_password}")
        return Response({"message": "New password sent to your phone number."}, status=status.HTTP_200_OK)
    except get_user_model().DoesNotExist:
        return Response({"detail": "Phone number not found."}, status=status.HTTP_404_NOT_FOUND)