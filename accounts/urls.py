from django.urls import path
from .views import register_patient, confirm_registration, login_user, logout_user, reset_password

urlpatterns = [
    path('register/', register_patient, name='register_patient'),
    path('confirm-registration/', confirm_registration, name='confirm_registration'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('reset-password/', reset_password, name='reset_password'),
]
