from rest_framework import generics
from ..models import ContainerCycleManagement
from ..serializers.container_cycle_serializers import ContainerCycleManagementSerializer

class ContainerCycleManagementListCreateView(generics.ListCreateAPIView):
    queryset = ContainerCycleManagement.objects.all()
    serializer_class = ContainerCycleManagementSerializer

class ContainerCycleManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContainerCycleManagement.objects.all()
    serializer_class = ContainerCycleManagementSerializer