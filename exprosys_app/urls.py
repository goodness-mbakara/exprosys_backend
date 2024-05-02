from django.urls import path
from .apis.register_api import RegisterView

from .apis.login_api import LoginView, ChangePasswordView, RecoverPasswordView, MyTokenObtainPairView
from .apis.containers_api import (
    ContainerListCreateAPIView, ContainerRetrieveUpdateDestroyAPIView, 
    ContainerEventListCreateAPIView, ContainerStatusAPIView,
    ContainerTransferAPIView, ContainerListView, ContainerDetailView)

from .apis.customer_api import CustomerListCreateAPIView, CustomerDetailView
from .apis.agency_apis import AgencyCreateView, AgencyListView, AgencyDetailView
from .apis.agent_api import AgentCreateView, AgentListView, AgentDetailView, AgentUpdateView

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
    #customer endpoints
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<str:customer_id>/', CustomerDetailView.as_view(), name='customer-detail'),
    #agency endpoints
    path('agency/', AgencyCreateView.as_view(), name='agency-create'),
    path('agency-list/', AgencyListView.as_view(), name='agency-list'),
    path('agency/<str:agency_id>/', AgencyDetailView.as_view(), name='agency-detail'),
    #agent endpoints
    path('agents/create/', AgentCreateView.as_view(), name='agent-create'),
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('agents/<str:agent_id>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agents/<str:agent_id>/update/', AgentUpdateView.as_view(), name='agent-update'),
]
