from django.db import models
import re
from django.core.exceptions import ValidationError
from accounts.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')))
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True, verbose_name="Previous Medical Conditions")  
    allergies = models.TextField(null=True, blank=True, verbose_name="Allergies") 
    past_surgeries = models.TextField(null=True, blank=True, verbose_name="Past Surgeries")  

    def save(self, *args, **kwargs):
        if self.height is not None and self.height < 0:
            raise ValidationError('Height cannot be negative.')
        if self.weight is not None and self.weight < 0:
            raise ValidationError('Weight cannot be negative.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.name}"
    def is_complete(self):
        return bool(self.first_name and self.last_name and self.birth_date and self.phone_number and self.address)
    


 class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    recommended_treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# patients/models.py (continued)
from django.db import models
from accounts.models import User

from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone
from datetime import datetime

class NotificationManager(models.Manager):
    def active(self):
        """ إرجاع فقط الإشعارات النشطة بعد تعطيل المنتهية """
        now = timezone.now()

        # تعطيل الإشعارات المنتهية
        self.filter(is_active=True, expiry_date__lt=now).update(is_active=False)

        # إرجاع الإشعارات النشطة فقط
        return self.filter(is_active=True)

from django.utils import timezone
from datetime import datetime

class Notification(models.Model):
    title = models.CharField(max_length=255)  # عنوان الإشعار
    message = models.TextField()  # محتوى الإشعار
    created_at = models.DateTimeField(auto_now_add=True)  # وقت الإنشاء
    expiry_date = models.DateTimeField()  # وقت انتهاء الإشعار
    is_active = models.BooleanField(default=True)  # تفعيل أو تعطيل الإشعار

    objects = NotificationManager()

    def save(self, *args, **kwargs):
        """ تعطيل الإشعار تلقائياً إذا انتهت صلاحيته """
        
        # إذا كانت قيمة expiry_date هي str، يجب تحويلها إلى datetime
        if isinstance(self.expiry_date, str):
            self.expiry_date = timezone.make_aware(datetime.strptime(self.expiry_date, "%Y-%m-%dT%H:%M:%SZ"))

        # إذا كانت مدة انتهاء الصلاحية قد مرّت بالفعل
        if self.expiry_date and self.expiry_date < timezone.now():
            self.is_active = False
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# patients/models.py (continued)
class Test(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    test_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True, max_length=500)

