from django.urls import path
from . import views
from .views import doctor_availability

urlpatterns = [
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('doctors/<int:doctor_id>/availability/', doctor_availability, name='doctor_availability'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
]
