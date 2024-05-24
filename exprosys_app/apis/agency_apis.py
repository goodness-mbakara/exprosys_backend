from rest_framework import generics
from ..models import Agency
from rest_framework.pagination import PageNumberPagination
from ..serializers.agency_serializers import AgencyListSerializer, AgencyDetailSerializer, AgencyCreateSerializer


class CustomPagination(PageNumberPagination):
    page_size = 17
    page_size_query_param = 'page_size'
    max_page_size = 100


class AgencyCreateView(generics.CreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyCreateSerializer

class AgencyListView(generics.ListAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyListSerializer
    pagination_class = CustomPagination  # Define this class to handle pagination settings

class AgencyDetailView(generics.RetrieveUpdateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    lookup_field = 'agency_id'

