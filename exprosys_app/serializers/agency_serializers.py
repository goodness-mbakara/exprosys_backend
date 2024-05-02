from rest_framework import serializers
from ..models import Agency

class AgencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['agency_id', 'agency_name', 'contact_person', 'email', 'phone_number', 'address']

class AgencyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'  # You can list all fields explicitly if needed

class AgencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
