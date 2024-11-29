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
    path('patient/<str:name>/', patient_details, name='patient-details'),
    path('<int:patient_id>/', patient_notifications, name='patient_notifications'),
    path('create_appointment_notification/<int:appointment_id>/', create_appointment_notification, name='create_appointment_notification'),
    path('create_medication_notification/<int:medication_id>/', create_medication_notification, name='create_medication_notification'),
    
    # إضافة المسارات الجديدة
    path('mark_notification_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('delete_notification/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('update_notification/<int:notification_id>/', update_notification, name='update_notification'),
]
