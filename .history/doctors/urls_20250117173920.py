from django.urls import path
from .views import doctor_list,create_doctor_account,doctors_by_department

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('list/', doctor_list, name='doctor_list'),
    # مسار الحصول على التوكن (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مسار تجديد التوكن
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # مساراتك الأخرى

    path('create/', create_doctor_account, name='create_doctor_account'),
    path('departments/<int:department_id>/doctors/', doctors_by_department, name='doctors_by_department'),


]
