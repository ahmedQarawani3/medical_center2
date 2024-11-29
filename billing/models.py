from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient
class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('paid', 'Paid')))
    payment_method = models.CharField(max_length=50, choices=(('credit_card', 'Credit Card'), ('paypal', 'PayPal')))
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
