from django.urls import path
from .apis.register_api import RegisterView

from .apis.login_api import LoginView, ChangePasswordView, RecoverPasswordView, MyTokenObtainPairView
from .apis.containers_api import (
    ContainerListCreateAPIView, ContainerRetrieveUpdateDestroyAPIView, 
    ContainerEventListCreateAPIView, ContainerStatusAPIView,
    ContainerTransferAPIView, ContainerListView, ContainerDetailView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('recover-password/', RecoverPasswordView.as_view(), name='recover_password'),
    path('containers/', ContainerListCreateAPIView.as_view(), name='container-list-create'),
    path('containers/<str:container_id>/', ContainerRetrieveUpdateDestroyAPIView.as_view(), name='container-detail'),
    path('containers/<str:container_id>/events/', ContainerEventListCreateAPIView.as_view(), name='container-events-list-create'),
    path('container-status/<str:container_id>/', ContainerStatusAPIView.as_view(), name='container-status'),
    path('container-transfer/', ContainerTransferAPIView.as_view(), name='container-transfer'),
    path('manage-containers/', ContainerListView.as_view(), name='container-manage'),
    path('manage-containers/<str:container_id>/', ContainerDetailView.as_view(), name='container-manage'),
]
