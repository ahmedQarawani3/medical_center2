# billing/urls.py
from django.urls import path
from .views import PaymentView, ManualPaymentView

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('manual-payment/', ManualPaymentView.as_view(), name='manual_payment'),
]
