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


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    specialization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True) 
    years_of_experience = models.PositiveIntegerField(default=0) 


class AssistantDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')))

