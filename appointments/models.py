from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient  
from doctors.models import  Doctor 
from datetime import datetime

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()   
    time_slot = models.DateTimeField( auto_now_add=True)  # وقت دقيق
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.doctor}"

    def can_cancel_or_reschedule(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        appointment_time = datetime.combine(self.date, self.time_slot)
        return appointment_time - timedelta(hours=8) > now
