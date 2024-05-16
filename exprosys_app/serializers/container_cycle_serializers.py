from rest_framework import serializers
from ..models import ContainerCycleManagement

class ContainerCycleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerCycleManagement
        fields = '__all__'