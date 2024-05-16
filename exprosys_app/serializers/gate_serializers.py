from rest_framework import serializers
from ..models import GateAccessControl, InboundPreGateEntry,OutboundGateExit

class GateAccessControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = GateAccessControl
        fields = '__all__'

class InboundPreGateEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundPreGateEntry
        fields = '__all__'


class OutboundGateExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboundGateExit
        fields = '__all__'



