from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from accounts.models import User
from .models import Department, Doctor
from .serializers import DoctorSerializer

# قائمة الأطباء
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.prefetch_related('availabilities').all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# doctors/views.py


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

    if not user_data or not doctor_data:
        return Response({"detail": "User and doctor data are required."}, status=status.HTTP_400_BAD_REQUEST)

    # التحقق من وجود رقم الهاتف أو اسم المستخدم
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
            role='doctor'  # تحديد أن المستخدم هو طبيب
        )
    except Exception as e:
        return Response({"detail": f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # إضافة حساب المستخدم إلى بيانات الطبيب
    doctor_data['user'] = user.id

    # التحقق من المواعيد وتضمينها في بيانات الطبيب
    availabilities_data = request.data.get('availabilities', [])
    if not availabilities_data:
        user.delete()
        return Response({"detail": "Availabilities data is required."}, status=status.HTTP_400_BAD_REQUEST)

    doctor_data['availabilities'] = availabilities_data
    doctor_serializer = DoctorSerializer(data=doctor_data)

    if doctor_serializer.is_valid():
        doctor_serializer.save()
    else:
        user.delete()  # حذف المستخدم إذا كان هناك خطأ في بيانات الطبيب
        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
