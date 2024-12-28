# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from accounts.serializer import UserRegistrationSerializer
from accounts.utils import send_sms
import random

# تخزين رموز التأكيد مؤقتاً
confirmation_codes = {}

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.utils import send_sms
from patients.models import Patient

confirmation_codes = {}

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from patients.models import Patient
from patients.serializers import PatientSerializer
from accounts.utils import send_sms  # يجب التأكد من وجود هذه الدالة لإرسال الرسائل

# تخزين رموز التفعيل مؤقتًا
confirmation_codes = {}

@api_view(['POST'])
def register_patient(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name')
    role = 'patient'

    if not phone_number or not password or not name:
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if get_user_model().objects.filter(phone_number=phone_number).exists():
        return Response({"detail": "Phone number already registered."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # إنشاء المستخدم باستخدام رقم الهاتف كـ username
        user = get_user_model().objects.create_user(
            username=phone_number,  # استخدام رقم الهاتف كـ username
            phone_number=phone_number,
            password=password
        )

        # توليد كود التفعيل بشكل عشوائي
        verification_code = str(random.randint(1000, 9999))  # كود عشوائي بين 1000 و 9999
        send_sms(phone_number, f"Your verification code is {verification_code}")

        # تخزين الكود مؤقتًا
        confirmation_codes[phone_number] = verification_code

        # إنشاء ملف تعريف المريض
        Patient.objects.create(user=user, name=name)

        return Response({"detail": "Patient registered successfully."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

# تخزين رموز التفعيل مؤقتًا
confirmation_codes = {}

@api_view(['POST'])
def confirm_registration(request):
    phone_number = request.data.get('phone_number')
    code = request.data.get('verification_code')

    if not phone_number or not code:
        return Response({"detail": "Phone number and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من وجود رقم الهاتف في رموز التفعيل المؤقتة
    if phone_number not in confirmation_codes:
        return Response({"detail": "Invalid phone number or code."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من تطابق الكود مع الكود المرسل
    if confirmation_codes[phone_number] == code:
        # العثور على المستخدم وتفعيل الحساب
        user = get_user_model().objects.get(phone_number=phone_number)
        user.is_active = True  # تفعيل الحساب
        user.save()

        # مسح الكود من الذاكرة بعد التحقق
        del confirmation_codes[phone_number]

        return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)






# accounts/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

@api_view(['POST'])
def login_user(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    role = request.data.get("role")

    if not phone_number or not password or not role:
        return Response({"detail": "Phone number, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من صحة بيانات المستخدم
    user = authenticate(request, username=phone_number, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # التحقق من أن الحساب مفعل
    if not user.is_active:
        return Response({"detail": "Account is not activated. Please confirm your account."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من الدور
    if user.role != role:
        return Response({"detail": "Role mismatch."}, status=status.HTTP_400_BAD_REQUEST)

    # إنشاء رموز التوثيق
    refresh = RefreshToken.for_user(user)
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

# accounts/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
from django.contrib.auth import get_user_model
from accounts.utils import send_sms

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