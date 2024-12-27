from django.contrib import admin

# Register your models here.

from .models import Medication
admin.site.register(Medication)

from .models import PrescriptionMedication
admin.site.register(PrescriptionMedication)