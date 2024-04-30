from rest_framework import generics
from ..models import Container, ContainerEvent
from ..serializers.container_serializers import ContainerSerializer, ContainerEventSerializer

class ContainerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    lookup_field = 'container_id'

class ContainerEventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ContainerEventSerializer

    def get_queryset(self):
        container_id = self.kwargs['container_id']
        return ContainerEvent.objects.filter(container__container_id=container_id)

    def perform_create(self, serializer):
        container_id = self.kwargs['container_id']
        container = generics.get_object_or_404(Container, container_id=container_id)
        serializer.save(container=container)
