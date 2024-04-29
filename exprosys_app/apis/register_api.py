from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers.registration_serializer import UserRegistrationSerializer

from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
