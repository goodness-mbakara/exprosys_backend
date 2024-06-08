from rest_framework import serializers
from ..models import ExportDelivery

class ExportDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportDelivery
        fields = '__all__'
