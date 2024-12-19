from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Doctor
from .serializers import DoctorSerializer

@api_view(['GET'])
def doctor_list(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from .models import Doctor
from .serializers import DoctorSerializer
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_doctor_account(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    user_data = request.data.get('user')
    doctor_data = request.data.get('doctor')

    if not user_data or not doctor_data:
        return Response({"detail": "User and doctor data are required."}, status=status.HTTP_400_BAD_REQUEST)

    # إنشاء حساب المستخدم
    try:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role='doctor'
        )
    except Exception as e:
        return Response({"detail": f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # البحث عن القسم باستخدام الاسم
    department_name = doctor_data.get('department')
    department = Department.objects.filter(name=department_name).first()

    if not department:
        user.delete()  # احذف المستخدم إذا لم يكن القسم موجودًا
        return Response({"detail": "Invalid department name."}, status=status.HTTP_400_BAD_REQUEST)

    # إضافة القسم للطبيب
    doctor_data['user'] = user.id
    doctor_data['department'] = department.id  # نربط القسم باستخدام المعرف
    serializer = DoctorSerializer(data=doctor_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        user.delete()  # إذا كان هناك خطأ، احذف المستخدم
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
