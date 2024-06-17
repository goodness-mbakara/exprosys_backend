from rest_framework import generics, permissions
from ..models import CustomUser, UserSession
from ..serializers.user_serializer import CustomUserSerializer, UserSessionSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class UserSessionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)
    
    