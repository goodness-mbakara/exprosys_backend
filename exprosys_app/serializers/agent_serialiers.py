from rest_framework import serializers
from ..models import Agent

class AgentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class AgentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
