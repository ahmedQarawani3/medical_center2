# appointments/models.py
from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time_slot = models.TimeField()  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('billing.Payment', on_delete=models.CASCADE, null=True, blank=True) 
    payment_transaction_id = models.CharField(max_length=255, null=True, blank=True) 

    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.doctor}"

    def can_cancel_or_reschedule(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        appointment_time = datetime.combine(self.date, datetime.min.time()) + timedelta(hours=self.time_slot.hour, minutes=self.time_slot.minute)
        return appointment_time - timedelta(hours=8) > now

    def is_payment_completed(self):
        return self.payment and self.payment.status == 'paid'
