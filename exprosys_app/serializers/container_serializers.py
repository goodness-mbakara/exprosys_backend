from rest_framework import serializers
from ..models import Container, ContainerEvent

class ContainerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerEvent
        fields = ['id', 'event_date', 'description']

class ContainerSerializer(serializers.ModelSerializer):
    events = ContainerEventSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ['container_id', 'container_size', 'container_type', 'status', 'current_location', 'origin', 'booking_number', 'estimated_arrival', 'shipping_line', 'events']
