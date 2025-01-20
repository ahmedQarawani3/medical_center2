# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    pattern = re.compile(r'^\+?\d{10,15}$')
    if not pattern.match(value):
        raise ValidationError('Phone number must be in the format +1234567890.')

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
]

class User(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone_number],
        error_messages={
            'unique': 'This phone number is already in use.',
        },
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"User: {self.phone_number}"

