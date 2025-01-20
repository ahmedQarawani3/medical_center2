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
from .serializers import DoctorSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Availability
from django.contrib.auth.models import User
from .serializers import DoctorSerializer

class create_doctor_account(APIView):
    def post(self, request):
        user_data = request.data.get("user")
        doctor_data = request.data.get("doctor")
        availabilities_data = request.data.get("availabilities")

        if not user_data or not doctor_data or not availabilities_data:
            return Response({"error": "User, Doctor, and Availabilities data are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # إنشاء المستخدم
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
            )
            # إنشاء الدكتور
            doctor = Doctor.objects.create(
                user=user,
                name=doctor_data["name"],
                specialty=doctor_data["specialty"],
                years_of_experience=doctor_data["years_of_experience"],
                consultation_fee=doctor_data["consultation_fee"],
                department=doctor_data["department"],
            )

            # إنشاء المواعيد وربطها بالدكتور
            for availability in availabilities_data:
                Availability.objects.create(
                    doctor=doctor,
                    day=availability["day"],
                    start_time=availability["start_time"],
                    end_time=availability["end_time"]
                )

            # عرض البيانات النهائية
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def doctors_by_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        doctors = Doctor.objects.filter(specialty=department.name)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
