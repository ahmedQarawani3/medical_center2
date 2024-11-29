from django.contrib import admin

# Register your models here.
from .models import Patient
admin.site.register(Patient)

from .models import MedicalRecord
admin.site.register(MedicalRecord)

from .models import Notification
admin.site.register(Notification)

from .models import Test
admin.site.register(Test)