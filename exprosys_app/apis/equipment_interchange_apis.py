from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import ContainerCycleManagement, ProcessEquipmentInterchange, EquipmentInterchangeReceipt
from ..serializers.equipment_interchange_serializers import  ProcessEquipmentInterchangeSerializer, EquipmentInterchangeReceiptSerializer


class ProcessEquipmentInterchangeListCreateView(generics.ListCreateAPIView):
    queryset = ProcessEquipmentInterchange.objects.all()
    serializer_class = ProcessEquipmentInterchangeSerializer

class ProcessEquipmentInterchangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProcessEquipmentInterchange.objects.all()
    serializer_class = ProcessEquipmentInterchangeSerializer

class EquipmentInterchangeReceiptListCreateView(generics.ListCreateAPIView):
    queryset = EquipmentInterchangeReceipt.objects.all()
    serializer_class = EquipmentInterchangeReceiptSerializer

class EquipmentInterchangeReceiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EquipmentInterchangeReceipt.objects.all()
    serializer_class = EquipmentInterchangeReceiptSerializer
