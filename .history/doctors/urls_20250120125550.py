from django.urls import path
from .views import doctors_by_department

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import DoctorListView,CreateDoctorAccountView

urlpatterns = [
    # مسار الحصول على التوكن (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مسار تجديد التوكن
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # مساراتك الأخرى

    path('create_doctor_account/', CreateDoctorAccountView.as_view(), name='create_doctor_account'),
    path('departments/<int:department_id>/doctors/', doctors_by_department, name='doctors_by_department'),
    path('list/', DoctorListView.as_view(), name='doctor-list'),




]
