from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from accounts.models import User
from .models import Department, Doctor
from .serializers import DoctorSerializer

# قائمة الأطباء
@api_view(['GET'])
def doctor_list(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)
# doctors/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Doctor, DoctorAvailability
from .serializers import DoctorAvailabilitySerializer
from accounts.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from doctors.models import Doctor, Availability
from accounts.models import User
from .serializers import DoctorSerializer, AvailabilitySerializer


@api_view(['POST'])
def create_doctor_account(request):
    user_data = request.data.get('user')
    doctor_data = request.data.get('doctor')
    availabilities_data = request.data.get('availabilities')

    if not user_data or not doctor_data or not availabilities_data:
        return Response({"detail": "User, doctor, and availabilities data are required."}, status=status.HTTP_400_BAD_REQUEST)

    # تحقق من وجود رقم الهاتف أو اسم المستخدم
    if User.objects.filter(phone_number=user_data['phone_number']).exists():
        return Response({"detail": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=user_data['username']).exists():
        return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # إنشاء حساب المستخدم
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            phone_number=user_data['phone_number'],
            role='doctor'  # حدد أن هذا المستخدم هو "طبيب"
        )
    except Exception as e:
        return Response({"detail": f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # إنشاء بيانات الطبيب
    doctor_data['user'] = user.id
    doctor_serializer = DoctorSerializer(data=doctor_data)

    if doctor_serializer.is_valid():
        doctor = doctor_serializer.save()
    else:
        user.delete()  # حذف المستخدم في حالة وجود خطأ في بيانات الطبيب
        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # إضافة مواعيد توافر الطبيب
    for availability in availabilities_data:
        availability['doctor'] = doctor.id
        availability_serializer = AvailabilitySerializer(data=availability)
        
        if availability_serializer.is_valid():
            availability_serializer.save()
        else:
            doctor.delete()  # حذف الطبيب في حالة وجود خطأ في مواعيد التوافر
            user.delete()  # حذف المستخدم
            return Response(availability_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def doctors_by_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        doctors = Doctor.objects.filter(specialty=department.name)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
