from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticates against the Django authentication system using either
    the username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get("email", None)
        if username:
            username=username.lower()
        if email is None and username is None:
            return None
        if email is not None:
            email = str(email).lower()
        credential = username or email
        
        user = UserModel.objects.filter(Q(username=credential)|Q(email=credential)).first()
        if user is None:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
