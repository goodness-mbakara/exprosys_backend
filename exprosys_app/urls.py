from django.urls import path
from .apis.register_api import RegisterView

from .apis.login_api import LoginView, ChangePasswordView, RecoverPasswordView, MyTokenObtainPairView
from .apis.containers_api import (
    ContainerListCreateAPIView, ContainerRetrieveUpdateDestroyAPIView, 
    ContainerEventListCreateAPIView, ContainerStatusAPIView,
    ContainerTransferAPIView, ContainerListView, ContainerDetailView)


from .apis.agency_apis import AgencyCreateView, AgencyListView, AgencyDetailView
from .apis.agent_api import AgentCreateView, AgentListView, AgentDetailView, AgentUpdateView
from .apis.truck_apis import TruckQueueManagementListCreateView,get_queue_metrics, TruckQueueManagementDetailView
from .apis.gate_apis import (GateAccessControlListCreateView,GateAccessControlDetailView,
    InboundPreGateEntryListCreateView,InboundPreGateEntryDetailView,OutboundGateExitListCreateView,OutboundGateExitDetailView)
from .apis.cointainer_cycle_apis import ContainerCycleManagementListCreateView,ContainerCycleManagementDetailView
from .apis.equipment_interchange_apis import (ProcessEquipmentInterchangeListCreateView,ProcessEquipmentInterchangeDetailView,EquipmentInterchangeReceiptListCreateView,EquipmentInterchangeReceiptDetailView,)
from .apis.invoice_apis import  PostExportInvoiceCreateView,PostPaymentCreateView,InvoicePostingReportDetailView
from .apis.booked_container_apis import BookedContainerListView
from .apis.exporter_api import ExporterListCreateView, ExporterRetrieveUpdateDestroyView
from .apis.export_delivery_api import ExportDeliveryListCreateView, ExportDeliveryRetrieveUpdateDestroyView

urlpatterns = [
    #auth endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(),name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('recover-password/', RecoverPasswordView.as_view(), name='recover_password'),
    #container endpoint
    path('containers/', ContainerListCreateAPIView.as_view(), name='container-list-create'),
    path('containers/<str:container_id>/', ContainerRetrieveUpdateDestroyAPIView.as_view(), name='container-detail'),
    path('containers/<str:container_id>/events/', ContainerEventListCreateAPIView.as_view(), name='container-events-list-create'),
    path('container-status/<str:container_id>/', ContainerStatusAPIView.as_view(), name='container-status'),
    path('container-transfer/', ContainerTransferAPIView.as_view(), name='container-transfer'),
    path('manage-containers/', ContainerListView.as_view(), name='container-manage'),
    path('manage-containers/<str:container_id>/', ContainerDetailView.as_view(), name='container-manage'),

    #agency endpoints
    path('agency/', AgencyCreateView.as_view(), name='agency-create'),
    path('agency-list/', AgencyListView.as_view(), name='agency-list'),
    path('agency/<str:agency_id>/', AgencyDetailView.as_view(), name='agency-detail'),
    #agent endpoints
    path('agents/create/', AgentCreateView.as_view(), name='agent-create'),
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('agents/<str:agent_id>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agents/<str:agent_id>/update/', AgentUpdateView.as_view(), name='agent-update'),
    #truck endpoints
    path('trucks/', TruckQueueManagementListCreateView.as_view(), name='truck-list-create'),
    path('trucks/<str:truck_id>/', TruckQueueManagementDetailView.as_view(), name='truck-detail'),
    path('queue-metrics/', get_queue_metrics, name='queue-metrics'),    
    #gate endpoints
    path('gate-access-controls/', GateAccessControlListCreateView.as_view(), name='gate-access-control-list-create'),
    path('gate-access-controls/<int:pk>/', GateAccessControlDetailView.as_view(), name='gate-access-control-detail'),

    path('inbound-pre-gate-entries/', InboundPreGateEntryListCreateView.as_view(), name='inbound-pre-gate-entry-list-create'),
    path('inbound-pre-gate-entries/<int:pk>/', InboundPreGateEntryDetailView.as_view(), name='inbound-pre-gate-entry-detail'),

    path('outbound-gate-exits/', OutboundGateExitListCreateView.as_view(), name='outbound-gate-exit-list-create'),
    path('outbound-gate-exits/<int:pk>/', OutboundGateExitDetailView.as_view(), name='outbound-gate-exit-detail'),
    
    #container cycle endpoints
    path('container-cycle/', ContainerCycleManagementListCreateView.as_view(), name='container-cycle-list'),
    path('container-cycle/<int:pk>/', ContainerCycleManagementDetailView.as_view(), name='container-cycle-detail'),
    
    #equipment interchange endpoints
    path('equipment-interchange/', ProcessEquipmentInterchangeListCreateView.as_view(), name='equipment-interchange-list'),
    path('equipment-interchange/<int:pk>/', ProcessEquipmentInterchangeDetailView.as_view(), name='equipment-interchange-detail'),
    path('interchange-receipt/', EquipmentInterchangeReceiptListCreateView.as_view(), name='interchange-receipt-list'),
    path('interchange-receipt/<int:pk>/', EquipmentInterchangeReceiptDetailView.as_view(), name='interchange-receipt-detail'),
    
    #invoice endpoints
    path('booked-containers/', BookedContainerListView.as_view(), name='booked-containers'),
    path('post-export-invoice/', PostExportInvoiceCreateView.as_view(), name='post-export-invoice'),
    path('post-payment/', PostPaymentCreateView.as_view(), name='post-payment'),
    path('invoice-posting-report/<int:pk>/', InvoicePostingReportDetailView.as_view(), name='invoice-posting-report'),
    
    #exporter endpoints
    path('exporters/', ExporterListCreateView.as_view(), name='exporter-list-create'),
    path('exporters/<int:pk>/', ExporterRetrieveUpdateDestroyView.as_view(), name='exporter-retrieve-update-destroy'),
    
    #export delivery endpoints
    path('export-deliveries/', ExportDeliveryListCreateView.as_view(), name='export-delivery-list-create'),
    path('export-deliveries/<int:pk>/', ExportDeliveryRetrieveUpdateDestroyView.as_view(), name='export-delivery-retrieve-update-destroy'),
]
