from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('orthopedics', 'عظمية'),
        ('gynecology', 'نسائية'),
        ('urology', 'بولية'),
        ('gastroenterology', 'هضمية'),
        ('nephrology', 'أمراض الكلى'),
        ('general_surgery and diabetic_foot', ' الجراحة العامة والقدم السكري'),
        ('ent', 'أمراض الأذن والأنف والحنجرة'),
        ('endocrinology', 'أمراض الغدد'),
        ('nutrition', 'التغذية'),
        ('dentistry', 'الأسنان وجراحتها'),
        ('cardiology', 'القلبية'),
        ('pulmonology', 'الأمراض الصدرية'),
        ('pediatrics', 'الأطفال'),
        ('dermatology', 'الجلدية'),
    ]

    name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
    )

    def __str__(self):
        return self.get_name_display()


from django.db import models

# doctors/models.py
from django.db import models
from accounts.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    available_days = models.JSONField(default=list)  # أيام متاحة مثل ['Monday', 'Wednesday', 'Friday']
    available_times = models.JSONField(default=list)  # أوقات متاحة مثل ['09:00', '14:00']
    years_of_experience = models.PositiveIntegerField(default=0) 
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)  # رسوم الاستشارة للطبيب

    def __str__(self):
        return self.name



class AssistantDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')))

