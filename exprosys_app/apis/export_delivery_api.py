from rest_framework import generics
from ..models import ExportDelivery
from ..serializers .export_delivery_serializer import ExportDeliverySerializer

class ExportDeliveryListCreateView(generics.ListCreateAPIView):
    queryset = ExportDelivery.objects.all()
    serializer_class = ExportDeliverySerializer

class ExportDeliveryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExportDelivery.objects.all()
    serializer_class = ExportDeliverySerializer
