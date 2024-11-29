from django.urls import path
from .views import register_patient, logout_user,login_user

urlpatterns = [
    path('register/', register_patient, name='register_patient'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]
