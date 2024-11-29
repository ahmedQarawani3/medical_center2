from django.db import models
from datetime import datetime, timedelta
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()   
    time_slot = models.TimeField()  # تم تغيير الحقل إلى TimeField
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.doctor}"

    def can_cancel_or_reschedule(self):
        """
        يتحقق ما إذا كان يمكن إلغاء أو تعديل الموعد
        """
        now = datetime.now()
        appointment_time = datetime.combine(self.date, self.time_slot)
        return appointment_time - timedelta(hours=8) > now
