from django.urls import path
from .views import doctor_list, department_list, doctors_in_department

urlpatterns = [
    path('list/', doctor_list, name='doctor_list'),  # عرض جميع الأطباء
    path('departments/', department_list, name='department_list'),  # عرض الأقسام
    path('department/<int:department_id>/', doctors_in_department, name='doctors_in_department'),  # عرض الأطباء حسب القسم
]
