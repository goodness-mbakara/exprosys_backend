from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        data.update({'email': self.user.email})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords must match"})
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
            self.context['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

    def validate(self, data):
        user = self.context.get('user')
        if user.account_recovery_question != data['recovery_question'] or user.account_recovery_answer.lower() != data['recovery_answer'].lower():
            raise serializers.ValidationError("Invalid security question or answer")

        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords must match"})

        validate_password(data['new_password'])
        return data

    def save(self, **kwargs):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user