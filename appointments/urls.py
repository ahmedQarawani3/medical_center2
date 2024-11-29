# appointments/urls.py
from django.urls import path
from .views import list_appointments, book_appointment, reschedule_appointment

urlpatterns = [
    path('appointments/', list_appointments, name='list_appointments'),  # عرض المواعيد المتاحة
    path('appointments/book/', book_appointment, name='book_appointment'),  # حجز موعد
    path('appointments/reschedule/<int:appointment_id>/', reschedule_appointment, name='reschedule_appointment'),  # إعادة جدولة الموعد
]
