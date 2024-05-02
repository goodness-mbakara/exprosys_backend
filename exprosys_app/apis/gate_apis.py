from rest_framework import generics
from ..models import GateAccessControl, InboundPreGateEntry,OutboundGateExit, TruckQueueManagement
from ..serializers.gate_serializers import GateAccessControlSerializer, InboundPreGateEntrySerializer,OutboundGateExitSerializer,TruckQueueManagementSerializer

class GateAccessControlListCreateView(generics.ListCreateAPIView):
    queryset = GateAccessControl.objects.all()
    serializer_class = GateAccessControlSerializer

class GateAccessControlDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GateAccessControl.objects.all()
    serializer_class = GateAccessControlSerializer

class InboundPreGateEntryListCreateView(generics.ListCreateAPIView):
    queryset = InboundPreGateEntry.objects.all()
    serializer_class = InboundPreGateEntrySerializer

class InboundPreGateEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InboundPreGateEntry.objects.all()
    serializer_class = InboundPreGateEntrySerializer

class OutboundGateExitListCreateView(generics.ListCreateAPIView):
    queryset = OutboundGateExit.objects.all()
    serializer_class = OutboundGateExitSerializer

class OutboundGateExitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutboundGateExit.objects.all()
    serializer_class = OutboundGateExitSerializer

class TruckQueueManagementListCreateView(generics.ListCreateAPIView):
    queryset = TruckQueueManagement.objects.all()
    serializer_class = TruckQueueManagementSerializer

class TruckQueueManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TruckQueueManagement.objects.all()
    serializer_class = TruckQueueManagementSerializer

