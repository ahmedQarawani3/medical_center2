import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from patients.models import Patient  # تأكد من استيراد نموذج المريض

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # مفتاح الـ Stripe

class PaymentView(APIView):
    def post(self, request):
        try:
            # تحقق من أن المستخدم هو مريض فقط
            if not hasattr(request.user, 'patient'):
                return Response({"error": "Only patients can make payments."}, status=status.HTTP_403_FORBIDDEN)
            
            # استلام البيانات من الـ Frontend
            doctor_id = request.data['doctor_id']
            amount = request.data['amount']
            payment_method = request.data['payment_method_id']

            # إنشاء PaymentIntent مع تمكين automatic_payment_methods
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # تحويل المبلغ إلى سنتات
                currency="usd",  # اختر العملة المناسبة
                payment_method=payment_method,
                confirm=True,
                automatic_payment_methods={
                    'enabled': True
                }
            )

            # حفظ الدفع في قاعدة البيانات (دون تعديل رصيد المريض)
            payment = Payment.objects.create(
                amount=amount,
                status='paid',
                transaction_id=intent.id,
                patient=request.user.patient
            )

            # إرجاع الـ client_secret إلى الـ Frontend لتأكيد الدفع
            return Response({"clientSecret": intent.client_secret}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
