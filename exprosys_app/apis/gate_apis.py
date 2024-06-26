from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import GateAccessControl, InboundPreGateEntry,OutboundGateExit
from ..serializers.gate_serializers import GateAccessControlSerializer, InboundPreGateEntrySerializer,OutboundGateExitSerializer
from django.db.models import Avg, Count, F, Q
from datetime import datetime, timedelta

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
