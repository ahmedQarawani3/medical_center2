from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
]
