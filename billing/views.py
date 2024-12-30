# billing/views.py
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from appointments.models import Appointment
from datetime import datetime
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment

# billing/views.py
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from appointments.models import Appointment
# billing/views.py
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# billing/views.py
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# billing/views.py
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]  # تأكد من أن المستخدم مسجل الدخول

    def post(self, request):
        try:
            if not hasattr(request.user, 'patient'):
                return Response({"error": "Only patients can make payments."}, status=status.HTTP_403_FORBIDDEN)
            doctor_id = request.data['doctor_id']
            amount = request.data['amount']
            payment_method = request.data['payment_method_id']

            # إنشاء PaymentIntent مع تمكين automatic_payment_methods
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # تحويل إلى سنتات
                currency="usd",
                payment_method=payment_method,
                confirm=True,
                automatic_payment_methods={
                    'enabled': True,  # تمكين الطرق التلقائية
                    'allow_redirects': 'never'  # تعطيل التوجيه التلقائي
                }
            )

            # حفظ الدفع
            payment = Payment.objects.create(
                amount=float(amount),
                status='paid',
                transaction_id=intent.id,
                patient=request.user.patient
            )

            return Response({"clientSecret": intent.client_secret}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment

class ManualPaymentView(APIView):
    def post(self, request):
        payment = Payment.objects.create(
            amount=request.data['amount'],
            status='paid',  # تعيين الحالة كمدفوع
            patient=request.data['patient_id'],
            transaction_id=request.data['transaction_id'],
            payment_date=request.data['payment_date']
        )
        return Response({"message": "Payment updated successfully."}, status=200)
