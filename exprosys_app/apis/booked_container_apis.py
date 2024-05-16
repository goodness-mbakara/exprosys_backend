from rest_framework import generics
from ..models import BookedContainer
from ..serializers.booked_container_serializers import BookedContainerSerializer

class BookedContainerListView(generics.ListAPIView):
    queryset = BookedContainer.objects.all()
    serializer_class = BookedContainerSerializer


