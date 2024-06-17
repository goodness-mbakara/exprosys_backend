from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import UserSession

User = get_user_model()


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id','device', 'location', 'browser', 'operating_system', 'time_of_entry']


class CustomUserSerializer(serializers.ModelSerializer):
    sessions = UserSessionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number', 'job_title', 'username', 'location_information', 
            'data_sharing', 'data_retention', 'data_storage', 'usage_analytics', 'payment_information', 
            'preferred_terminal_team', 'language_preference', 'accessibility_preference', 'account_recovery_email', 
            'account_recovery_phone', 'account_recovery_question', 'account_recovery_answer', 'is_active', 
            'profile_picture', 'gender', 'language', 'display_name', 'country_region', 'sessions'
        ]
