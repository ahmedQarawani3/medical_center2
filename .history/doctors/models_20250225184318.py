from django.db import models
from accounts.models import User

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('orthopedics', 'عظمية'),
        ('gynecology', 'نسائية'),
        ('urology', 'بولية'),
        ('gastroenterology', 'هضمية'),
        ('nephrology', 'أمراض الكلى'),
        ('general_surgery_and_diabetic_foot', 'الجراحة العامة والقدم السكري'),
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
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        unique=True
    )

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.get_name_display()


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor', unique=True)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return self.name





from django.db import models
from doctors.models import Doctor


class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time} - {self.end_time}"



class AssistantDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')))

