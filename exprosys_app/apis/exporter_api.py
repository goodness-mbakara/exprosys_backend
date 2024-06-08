from rest_framework import generics
from ..models import Exporter
from ..serializers.exporter_serializer import ExporterSerializer
from ..pagination import ExporterPagination

class ExporterListCreateView(generics.ListCreateAPIView):
    queryset = Exporter.objects.all()
    serializer_class = ExporterSerializer
    pagination_class = ExporterPagination

class ExporterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exporter.objects.all()
    serializer_class = ExporterSerializer
