from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=100)

class PrescriptionMedication(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication)
    date_issued = models.DateField()
    quantity = models.PositiveIntegerField()  

