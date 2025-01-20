from django.urls import path
from . import views
from .views import doctor_availability
from . views import 
urlpatterns = [
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('doctors/<int:doctor_id>/availability/', doctor_availability, name='doctor_availability'),
    path('doctors/department/<str:department_name>/', BookAppointmentView, name='list_doctors_by_department'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
]
