from django.urls import path
 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import DoctorListView , create_doctor_account
from .views import list_departments
from .views import list_doctors_by_department
from . import views


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_doctor_account/', create_doctor_account.as_view(), name='create_doctor_account'),#انشاء دكتور
    path('list/', DoctorListView.as_view(), name='doctor-list'),#عرض الدكاتره 
    path('departments/', list_departments, name='list_departments'),  #عرض الاقسام
    path('doctors/department/<str:department_name>/', list_doctors_by_department, name='list_doctors_by_department'),#عرض الدكاتره حسب القسم
    path('doctors/<int:doctor_id>/availabilities/', views.get_doctor_availabilities, name='doctor_availabilities'),#عرض الاوقات المتاحه للدكتور
]
