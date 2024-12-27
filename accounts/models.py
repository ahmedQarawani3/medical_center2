# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

    def is_admin(self):
        return self.role == 'admin'
