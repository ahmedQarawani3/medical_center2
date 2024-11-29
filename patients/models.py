from django.db import models
from accounts.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')))
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.name}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    recommended_treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('appointment', 'Appointment'),
        ('test', 'Test'),
        ('medication', 'Medication'),
    )

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    notification_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # الحقل الجديد لتحديد ما إذا كان تم قراءة الإشعار
    
    def mark_as_read(self):
        self.read = True
        self.save()


class Test(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    test_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
