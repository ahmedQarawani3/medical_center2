# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializer import UserRegistrationSerializer
from patients.serializers import PatientSerializer
from patients.models import Patient

@api_view(['POST'])
def register_patient(request):
    user_serializer = UserRegistrationSerializer(data=request.data.get('user'))
    patient_serializer = PatientSerializer(data=request.data.get('patient'))

    if user_serializer.is_valid() and patient_serializer.is_valid():
        user = user_serializer.save(role='patient')
        patient_serializer.save(user=user)
        return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
    return Response({'user_errors': user_serializer.errors, 'patient_errors': patient_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)

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

    if not user.is_active:
        return Response({"detail": "Account is inactive."}, status=status.HTTP_403_FORBIDDEN)

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
