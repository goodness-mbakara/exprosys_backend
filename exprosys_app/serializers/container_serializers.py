from rest_framework import serializers
from ..models import Container, ContainerEvent, ContainerTransfer


class ContainerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerEvent
        fields = ['event_date', 'description']

class ContainerSerializer(serializers.ModelSerializer):
    events = ContainerEventSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ['container_id', 'container_size', 'container_type', 'status', 'current_location', 'origin', 'booking_number', 'estimated_arrival', 'shipping_line', 'events']

class ContainerDetailSerializer(serializers.ModelSerializer):
    events = ContainerEventSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ['container_id', 'container_type', 'current_location', 'status', 'origin', 'booking_number', 'estimated_arrival', 'shipping_line', 'events']

class ContainerTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerTransfer
        fields = ['container', 'transfer_from', 'transfer_to', 'transfer_date', 'confirmation_code', 'reasons_for_transfer']

    def validate(self, data):
        # Ensure that the transfer_from matches the container's current location
        container = data['container']
        if data['transfer_from'] != container.current_location:
            raise serializers.ValidationError("Transfer from location must match the container's current location.")
        return data

    def create(self, validated_data):
        # Update the container's current location after the transfer
        container_transfer = ContainerTransfer.objects.create(**validated_data)
        container = validated_data['container']
        container.current_location = validated_data['transfer_to']
        container.save()

        return container_transfer
