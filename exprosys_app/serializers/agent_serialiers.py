from rest_framework import serializers
from ..models import Agent

class AgentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['agent_id', 'agent_name', 'contact_person', 'email', 'phone_number', 'address']

class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['profile_picture', 'agency_name', 'id', 'address', 'email', 'phone_number', 'services_offered']

class AgentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
