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

# إنشاء حساب طبيب
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doctor_account(request):
    # تحقق من أن المستخدم لديه صلاحيات المسؤول
    if request.user.role != 'admin':
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    user_data = request.data.get('user')
    doctor_data = request.data.get('doctor')

    # تحقق من أن بيانات المستخدم والطبيب موجودة
    if not user_data or not doctor_data:
        return Response({"detail": "User and doctor data are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # إنشاء المستخدم الجديد
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role='doctor'
        )
    except Exception as e:
        return Response({"detail": f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # استرجاع القسم بناءً على الاسم
    department_name = doctor_data.get('department')
    department = Department.objects.filter(name=department_name).first()

    if not department:
        return Response({"detail": "Invalid department name."}, status=status.HTTP_400_BAD_REQUEST)

    # إعداد بيانات الطبيب
    doctor_data['user'] = user.id
    serializer = DoctorSerializer(data={
        "user": user.id,
        "department": department.id,
        "specialization": doctor_data.get('specialization'),
        "years_of_experience": doctor_data.get('years_of_experience')
    })

    # تحقق من صحة البيانات
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # حذف المستخدم في حالة وجود خطأ في بيانات الطبيب
        user.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
