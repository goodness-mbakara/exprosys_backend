from ..models import TruckQueueManagement
from rest_framework import serializers

class TruckQueueManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckQueueManagement
        fields = '__all__'