# urls.py
from django.urls import path
from .views import UpdatePatientProfileView
from .views import CreateNotificationView, ListNotificationsView

from .views import (
    patient_details,


    
)

urlpatterns = [
    path('patient/details/<str:name>/', patient_details, name='patient_details'),
    path('create/', CreateNotificationView.as_view(), name='create-notification'),  # إضافة إشعار (Admin فقط)
    path('list/', ListNotificationsView.as_view(), name='list-notifications'),  # عرض جميع الإشعارات (للمرضى)
    path('profile/', UpdatePatientProfileView.as_view(), name='update-patient-profile'),


]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
