import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from patients.models import Patient  # تأكد من استيراد نموذج المريض

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # تحديد المفتاح الخاص بـ Stripe من الإعدادات

from decimal import Decimal

class PaymentView(APIView):
    def post(self, request):
        try:
            # التأكد من أن المستخدم هو مريض
            if not hasattr(request.user, 'patient'):
                return Response({"error": "Only patients can make payments."}, status=status.HTTP_403_FORBIDDEN)

            doctor_id = request.data['doctor_id']
            amount = request.data['amount']
            payment_method = request.data['payment_method_id']

            # إنشاء PaymentIntent مع تمكين automatic_payment_methods
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # تحويل المبلغ إلى سنتات
                currency="usd",
                payment_method=payment_method,
                confirm=True,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'  
                }
            )

            payment = Payment.objects.create(
                amount=float(amount),
                status='paid',
                transaction_id=intent.id,
                patient=request.user.patient
            )

            return Response({"clientSecret": intent.client_secret}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
