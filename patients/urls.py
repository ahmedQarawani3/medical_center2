# urls.py
from django.urls import path
from .views import (
    patient_details,
    patient_notifications,
    create_appointment_notification,
    create_medication_notification,
    get_notifications,
    mark_notification_as_read,
    delete_notification,
    update_notification,
)

urlpatterns = [
    path('notifications/', get_notifications, name='get_notifications'),
    path('patient/details/<str:name>/', patient_details, name='patient_details'),
    path('patient/<int:patient_id>/notifications/', patient_notifications, name='patient_notifications'),
    path('notification/create/appointment/<int:appointment_id>/', create_appointment_notification, name='create_appointment_notification'),
    path('notification/create/medication/<int:medication_id>/', create_medication_notification, name='create_medication_notification'),
    path('notification/read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('notification/update/<int:notification_id>/', update_notification, name='update_notification'),
]