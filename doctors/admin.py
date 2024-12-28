from django.contrib import admin

# Register your models here.
from .models import Doctor
admin.site.register(Doctor)

from .models import Department
admin.site.register(Department)

from .models import AssistantDoctor
admin.site.register(AssistantDoctor)