from django.urls import path
from .apis.register_api import RegisterView

from .apis.login_api import LoginView, ChangePasswordView, RecoverPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('recover-password/', RecoverPasswordView.as_view(), name='recover_password'),
]
