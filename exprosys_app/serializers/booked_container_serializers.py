from rest_framework import serializers
from ..models import BookedContainer
class BookedContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedContainer
        fields = '__all__'


