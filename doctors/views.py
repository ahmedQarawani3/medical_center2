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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doctor_account(request):
    if request.user.role != 'admin':  # تحقق من أن المستخدم هو "مسؤول"
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    user_data = request.data.get('user')
    doctor_data = request.data.get('doctor')

    if not user_data or not doctor_data:
        return Response({"detail": "User and doctor data are required."}, status=status.HTTP_400_BAD_REQUEST)

    # تحقق من وجود رقم الهاتف أو اسم المستخدم
    if User.objects.filter(phone_number=user_data['phone_number']).exists():
        return Response({"detail": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=user_data['username']).exists():
        return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            phone_number=user_data['phone_number'],  # التأكد من رقم الهاتف
            role='doctor'
        )
    except Exception as e:
        return Response({"detail": f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    department_name = doctor_data.get('department')
    department = Department.objects.filter(name=department_name).first()

    if not department:
        return Response({"detail": "Invalid department name."}, status=status.HTTP_400_BAD_REQUEST)

    doctor_data['user'] = user.id
    serializer = DoctorSerializer(data={
        "user": user.id,
        "name":doctor_data.get('name'),
        "specialty": doctor_data.get('specialization'),
        "available_days": doctor_data.get('available_days', []),
        "available_times": doctor_data.get('available_times', []),
        "years_of_experience": doctor_data.get('years_of_experience', 0),
        "consultation_fee": doctor_data.get('consultation_fee', 0.0),
    })

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        user.delete()  # حذف المستخدم في حالة وجود خطأ في بيانات الطبيب
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

