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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doctor_availability(request):
    if request.user.role != 'admin':  # تحقق من أن المستخدم هو "مسؤول"
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    doctor_data = request.data.get('doctor')
    availabilities_data = request.data.get('availabilities')

    if not doctor_data or not availabilities_data:
        return Response({"detail": "Doctor and availability data are required."}, status=status.HTTP_400_BAD_REQUEST)

    # تحقق من أن الطبيب موجود
    doctor = Doctor.objects.filter(id=doctor_data['doctor_id']).first()
    if not doctor:
        return Response({"detail": "Doctor not found."}, status=status.HTTP_400_BAD_REQUEST)

    # حفظ الأوقات المتاحة للطبيب
    availability_objects = []
    for availability in availabilities_data:
        day = availability.get('day')
        start_time = availability.get('start_time')
        end_time = availability.get('end_time')

        if not day or not start_time or not end_time:
            return Response({"detail": "Day, start time, and end time are required for each availability."}, status=status.HTTP_400_BAD_REQUEST)

        availability_object = DoctorAvailability(
            doctor=doctor,
            day=day,
            start_time=start_time,
            end_time=end_time
        )
        availability_objects.append(availability_object)

    # حفظ الأوقات دفعة واحدة
    DoctorAvailability.objects.bulk_create(availability_objects)

    return Response({"detail": "Doctor availability successfully created."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def doctors_by_department(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        doctors = Doctor.objects.filter(specialty=department.name)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
