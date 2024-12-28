# billing/models.py
from django.db import models
from patients.models import Patient

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.status} for {self.patient.name}"
