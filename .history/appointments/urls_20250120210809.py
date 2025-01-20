from django.urls import path
from . import views
from .views import doctor_availability
from .views import BookAppointmentView
urlpatterns = [
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('doctors/<int:doctor_id>/availability/', doctor_availability, name='doctor_availability'),
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
]
