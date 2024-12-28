from django.shortcuts import render

# Create your views here.
# billing/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer

class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # يمكن هنا إضافة منطق معالجة الدفع مثل التحقق من بوابة الدفع
            payment = serializer.save()
            return Response({"message": "Payment created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# billing/views.py
import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentView(APIView):
    def post(self, request):
        try:
            # إعداد المبلغ
            amount = 5000  # مثلاً 50.00 USD
        
            # إنشاء الدفع عبر Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=request.data.get('payment_method_id'),
                confirmation_method='manual',
                confirm=True,
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except stripe.error.CardError as e:
            return JsonResponse({"error": str(e)}, status=400)

# billing/views.py
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