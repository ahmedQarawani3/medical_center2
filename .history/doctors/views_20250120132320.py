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
        doctors = Doctor.objects.all()  # جلب جميع الأطباء
        serializer = DoctorSerializer(doctors, many=True)  # تحويل إلى JSON
        return Response(serializer.data, status=status.HTTP_200_OK)
 
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .models import Doctor, Availability
from .serializers import DoctorSerializer
from rest_framework.views import APIView

 

class create_doctor_account(APIView):
    def post(self, request):
        # التحقق من أن المستخدم هو المسؤول
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to create a doctor account."}, status=status.HTTP_403_FORBIDDEN)

        user_data = request.data.get("user")
        doctor_data = request.data.get("doctor")
        availabilities_data = request.data.get("availabilities")

        if not user_data or not doctor_data or not availabilities_data:
            return Response({"error": "User, Doctor, and Availabilities data are required."}, status=status.HTTP_400_BAD_REQUEST)

        # تحقق من تكرار اسم المستخدم
        if User.objects.filter(username=user_data["username"]).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # تحقق من تكرار رقم الهاتف
        if User.objects.filter(phone_number=user_data["phone_number"]).exists():
            return Response({"error": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # إنشاء المستخدم
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                phone_number=user_data["phone_number"]
            )
            # تعيين المستخدم كطبيب
            user.role = 'doctor'  # تحديد دور المستخدم كـ "طبيب"
            user.save()

            # إنشاء الدكتور
            doctor = Doctor.objects.create(
                user=user,
                name=doctor_data["name"],
                specialty=doctor_data["specialty"],
                years_of_experience=doctor_data["years_of_experience"],
                consultation_fee=doctor_data["consultation_fee"],
                department=doctor_data["department"],
            )

            # إنشاء المواعيد
            for availability in availabilities_data:
                Availability.objects.create(
                    doctor=doctor,
                    day=availability["day"],
                    start_time=availability["start_time"],
                    end_time=availability["end_time"]
                )

            # عرض بيانات الطبيب بعد الإنشاء
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)







# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer

@api_view(['GET'])
def list_departments(request):
    # جلب جميع الأقسام من قاعدة البيانات
    departments = Department.objects.all()
    
    # إذا لم توجد أي أقسام في قاعدة البيانات
    if not departments:
        return Response({"detail": "No departments found."}, status=status.HTTP_404_NOT_FOUND)
    
    # استخدام الـ Serializer لتحويل الأقسام إلى JSON
    serializer = DepartmentSerializer(departments, many=True)
    
    # إرجاع الأقسام بشكل JSON
    return Response(serializer.data, status=status.HTTP_200_OK)


 
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer

@api_view(['GET'])
def list_doctors_by_department(request, department_name):
    # البحث عن الأطباء حسب القسم
    doctors = Doctor.objects.filter(department=department_name)
    
    # إذا لم توجد أي أطباء في هذا القسم
    if not doctors:
        return Response({"detail": "No doctors found in this department."}, status=status.HTTP_404_NOT_FOUND)
    
    # استخدام الـ Serializer لتحويل الأطباء إلى JSON
    serializer = DoctorSerializer(doctors, many=True)
    
    # إرجاع الأطباء بشكل JSON
    return Response(serializer.data, status=status.HTTP_200_OK)


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Availability
from .serializers import AvailabilitySerializer

@api_view(['GET'])
def get_doctor_availabilities(request, doctor_id):
    """
    عرض مواعيد التوافر الخاصة بالطبيب
    """
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # جلب مواعيد التوافر للطبيب
    availabilities = Availability.objects.filter(doctor=doctor)

    # تفعيل السيرياليزر لتحويل البيانات إلى JSON
    availability_serializer = AvailabilitySerializer(availabilities, many=True)

    return Response(availability_serializer.data, status=status.HTTP_200_OK)
