from rest_framework import generics
from ..models import Container, ContainerEvent, ContainerTransfer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers.container_serializers import (
    ContainerSerializer, ContainerEventSerializer, 
    ContainerDetailSerializer, ContainerTransferSerializer, ContainerListSerializer, ManageContainerDetailSerializer
)

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

class ContainerStatusAPIView(APIView):
    """
    Retrieve detailed information about a container including current status, location, and events.
    """

    def get(self, request, container_id):
        container = Container.objects.filter(container_id=container_id).first()
        if container:
            serializer = ContainerDetailSerializer(container)
            return Response(serializer.data)
        else:
            return Response({"error": "Container not found"}, status=status.HTTP_404_NOT_FOUND)

class ContainerTransferAPIView(generics.CreateAPIView):
    queryset = ContainerTransfer.objects.all()
    serializer_class = ContainerTransferSerializer


class ContainerListView(generics.ListAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerListSerializer

class ContainerDetailView(APIView):
    def get(self, request, container_id):
        container = Container.objects.filter(container_id=container_id).first()
        if container:
            serializer = ManageContainerDetailSerializer(container)
            return Response(serializer.data)
        else:
            return Response({'error': 'Container not found'}, status=status.HTTP_404_NOT_FOUND)