from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user_agents import parse

from ..models import UserSession

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # super().email = serializers.EmailField(required=False)
    # credential = serializers.CharField(required=False)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token["username"] = user.username
        token["email"] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Create a user session
        request = self.context["request"]
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        device = f"{user_agent.device.family} {user_agent.device.brand} {user_agent.device.model}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        operating_system = f"{user_agent.os.family} {user_agent.os.version_string}"
        location = request.META.get('REMOTE_ADDR')  # In production, use a proper geolocation service

        user = self.user

        # Use the access token for session token
        refresh = RefreshToken.for_user(user)
        session_token = str(refresh.access_token)

        UserSession.objects.create(
            user=user,
            device=device,
            location=location,
            browser=browser,
            operating_system=operating_system,
            session_token=session_token,
            time_of_entry=timezone.now()
        )

        data["refresh"] = str(refresh)
        data["access"] = session_token
        data["username"] = user.username
        data["email"] = user.email

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New passwords must match"}
            )
        return data


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    recovery_question = serializers.CharField(required=True)
    recovery_answer = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            self.context["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

    def validate(self, data):
        user = self.context.get("user")
        if (
            user.account_recovery_question != data["recovery_question"]
            or user.account_recovery_answer.lower() != data["recovery_answer"].lower()
        ):
            raise serializers.ValidationError("Invalid security question or answer")

        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New passwords must match"}
            )

        validate_password(data["new_password"])
        return data

    def save(self, **kwargs):
        user = self.context["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
