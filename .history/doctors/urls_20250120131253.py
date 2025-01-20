from django.urls import path
from .views import doctors_by_department

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import DoctorListView , create_doctor_account

urlpatterns = [
    # مسار الحصول على التوكن (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مسار تجديد التوكن
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # مساراتك الأخرى

    path('create_doctor_account/', create_doctor_account.as_view(), name='create_doctor_account'),
     path('list/', DoctorListView.as_view(), name='doctor-list'),




]
