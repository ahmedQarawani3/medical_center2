from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import TemporaryBooking, Booking
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentAPI(APIView):
    def post(self, request, booking_id):
        # جلب الحجز المؤقت
        booking = get_object_or_404(TemporaryBooking, id=booking_id)

        try:
            # إنشاء طلب دفع عبر Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(booking.amount_due * 100),  # تحويل المبلغ إلى سنت
                currency='usd',
                metadata={'booking_id': booking.id}
            )
            return Response({
                'clientSecret': payment_intent.client_secret
            }, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentAPI(APIView):
    def post(self, request):
        payment_intent_id = request.data.get('payment_intent_id')
        booking_id = request.data.get('booking_id')

        try:
            # جلب الدفع المؤقت
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            booking = get_object_or_404(TemporaryBooking, id=booking_id)

            if payment_intent.status == 'succeeded':
                # تحديث حالة الحجز إلى "مدفوع"
                booking.status = 'paid'
                booking.save()

                # إنشاء حجز مؤكد في النظام
                confirmed_booking = Booking.objects.create(
                    patient=booking.patient,
                    doctor=booking.doctor,
                    appointment_time=booking.appointment_time,
                    amount_due=booking.amount_due
                )
                return Response({'message': 'Payment successful, booking confirmed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
