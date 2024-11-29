from django.urls import path
from .views import doctor_list

urlpatterns = [
    path('list/', doctor_list, name='doctor_list'),
]
