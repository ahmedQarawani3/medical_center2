from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from patients.models import Patient

@api_view(['POST'])
def register_patient(request):
    try:
        user_data = request.data.get('user')
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')

        if User.objects.filter(username=username).exists():
            raise ValidationError('اسم المستخدم موجود بالفعل.')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='patient' 
        )

        patient_data = request.data
        patient = Patient.objects.create(
            user=user,
            date_of_birth=str(patient_data.get('date_of_birth')),
            phone_number=patient_data.get('phone_number'),
            address=patient_data.get('address'),
            name=patient_data.get('name'),
            gender=patient_data.get('gender'),
            height=patient_data.get('height'),
            weight=patient_data.get('weight')
        )
        return Response({'message': 'تم إنشاء الحساب بنجاح.'}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")

    if not username or not password or not role:
        return Response({"detail": "Username, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    if user.role != role:
        return Response({"detail": "Invalid role."}, status=status.HTTP_403_FORBIDDEN)

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


@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")  # دور المستخدم يجب أن يكون موجودًا

    if not username or not password or not role:
        return Response({"detail": "Username, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    if user.role != role:
        return Response({"detail": "Invalid role."}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        "access": access_token,
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)
