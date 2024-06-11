from rest_framework import serializers
from ..models import Container, ContainerEvent, ContainerTransfer
from .exporter_serializer import ExporterSerializer

class ContainerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerEvent
        fields = ['event_date', 'description']

class ContainerSerializer(serializers.ModelSerializer):
    #events = ContainerEventSerializer(many=True, read_only=True)
    exporter = ExporterSerializer(read_only = True, many = True)

    class Meta:
        model = Container
        fields ='__all__' #['container_id', 'container_size', 'container_type', 'status', 'current_location', 'origin', 'booking_number', 'estimated_time_of_arrival', 'shipping_line', 'events']

class ContainerDetailSerializer(serializers.ModelSerializer):
    events = ContainerEventSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ['container_id', 'container_type', 'current_location', 'status', 'origin', 'booking_number', 'estimated_time_of_arrival', 'shipping_line', 'events']

class ContainerTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerTransfer
        fields = ['container', 'transfer_from', 'transfer_to', 'transfer_date', 'confirmation_code', 'reasons_for_transfer']

    def validate(self, data):
        # Ensure that the transfer_from matches the container's current location
        container = data['container']
        if data['transfer_from'] != container.origin:
            raise serializers.ValidationError("Transfer from location must match the container's current location.")
        return data

    def create(self, validated_data):
        # Update the container's current location after the transfer
        container_transfer = ContainerTransfer.objects.create(**validated_data)
        container = validated_data['container']
        container.origin = validated_data['transfer_to']
        container.save()

        return container_transfer

class ContainerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__' #['container_id', 'status', 'container_type', 'arrival_date', 'departure_date', 'vessel_name', 'exporter_name']

class ManageContainerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['container_id', 'arrival_date', 'departure_date', 'origin', 'destination', 'status', 'vessel_assignment', 'cargo_type', 'last_update', 'estimated_time_of_arrival']
