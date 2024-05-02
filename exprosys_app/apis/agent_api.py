from rest_framework import generics
from ..models import Agent
from ..serializers.agent_serialiers import AgentListSerializer, AgentDetailSerializer, AgentCreateUpdateSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 17
    page_size_query_param = 'page_size'
    max_page_size = 100

class AgentCreateView(generics.CreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentCreateUpdateSerializer

class AgentListView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentListSerializer
    pagination_class = CustomPagination

class AgentDetailView(generics.RetrieveAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentDetailSerializer
    lookup_field = 'agent_id'

class AgentUpdateView(generics.UpdateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentCreateUpdateSerializer
    lookup_field = 'agent_id'
