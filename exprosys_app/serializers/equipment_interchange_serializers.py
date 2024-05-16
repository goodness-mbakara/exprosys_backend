from rest_framework import serializers
from ..models import  ProcessEquipmentInterchange, EquipmentInterchangeReceipt


class ProcessEquipmentInterchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessEquipmentInterchange
        fields = '__all__'

class EquipmentInterchangeReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentInterchangeReceipt
        fields = '__all__'
