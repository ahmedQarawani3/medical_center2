from django.urls import path
from .views import DepartmentListView, DoctorListView, AppointmentListView, CreateAppointmentView, ConfirmPaymentView

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('doctors/<int:department_id>/', DoctorListView.as_view(), name='doctor-list'),
    path('appointments/<int:doctor_id>/', AppointmentListView.as_view(), name='appointment-list'),
    path('create-appointment/<int:doctor_id>/', CreateAppointmentView.as_view(), name='create-appointment'),
   
]
