from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Department
from .serializers import DoctorSerializer, DepartmentSerializer

@api_view(['GET'])
def doctor_list(request):
  
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def department_list(request):
    """
    عرض جميع الأقسام
    """
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def doctors_in_department(request, department_id):
    """
    عرض الأطباء حسب القسم
    """
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

    doctors = Doctor.objects.filter(department=department)
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)
