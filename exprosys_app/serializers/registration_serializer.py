from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name', 'phone_number', 'job_title', 'location_information', 'data_sharing', 'data_retention', 'data_storage', 'usage_analytics', 'payment_information', 'preferred_terminal_team', 'language_preference', 'accessibility_preference', 'account_recovery_email', 'account_recovery_phone', 'account_recovery_question', 'account_recovery_answer']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
