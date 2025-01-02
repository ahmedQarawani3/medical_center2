import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Doctor, Appointment, Payment
from .serializers import DepartmentSerializer, DoctorSerializer, AppointmentSerializer, PaymentSerializer
from django.contrib.auth.models import User


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# 1. عرض الأقسام
class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    
# 2. عرض الأطباء حسب القسم
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListView(APIView):
    def get(self, request, department_id):
        doctors = Doctor.objects.filter(department_id=department_id)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    
    
# 3. عرض المواعيد المتاحة للطبيب
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Appointment
from .serializers import AppointmentSerializer

class AppointmentListView(APIView):
    def get(self, request, doctor_id):
        # جلب المواعيد المتاحة للطبيب
        appointments = Appointment.objects.filter(doctor_id=doctor_id, status='available')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    
# 4. حجز موعد
class CreateAppointmentView(APIView):
    def post(self, request, doctor_id):
        patient = request.user  # assuming user is logged in
        date = request.data.get('date')
        time = request.data.get('time')

        # تحقق إذا كان الموعد متاحًا
        appointment = Appointment.objects.filter(doctor_id=doctor_id, date=date, time=time, status='available').first()

        if not appointment:
            return Response({"error": "Appointment is not available."}, status=status.HTTP_400_BAD_REQUEST)

        # الحصول على قيمة المعاينة للطبيب
        doctor = Doctor.objects.get(id=doctor_id)
        consultation_fee = doctor.consultation_fee

        # إنشاء الحجز
        appointment.status = 'booked'
        appointment.patient = patient
        appointment.save()

        # حفظ تفاصيل الدفع
        payment = Payment.objects.create(appointment=appointment, amount=consultation_fee)
        payment_serializer = PaymentSerializer(payment)

        return Response({
            "message": "Appointment booked successfully, please complete the payment.",
            "payment": payment_serializer.data,
            "consultation_fee": consultation_fee
        }, status=status.HTTP_201_CREATED)
