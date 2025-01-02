from django.urls import path
from .views import CreatePaymentIntentAPI, ConfirmPaymentAPI

urlpatterns = [
    path('create-payment-intent/<int:booking_id>/', CreatePaymentIntentAPI.as_view(), name='create-payment-intent'),
    path('confirm-payment/', ConfirmPaymentAPI.as_view(), name='confirm-payment'),
]
