from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        #user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    job_title = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    location_information = models.BooleanField(default=False)
    data_sharing = models.BooleanField(default=False)
    data_retention = models.BooleanField(default=False)
    data_storage = models.BooleanField(default=False)
    usage_analytics = models.BooleanField(default=False)
    payment_information = models.BooleanField(default=False)
    preferred_terminal_team = models.CharField(max_length=150)
    language_preference = models.CharField(max_length=150)
    accessibility_preference = models.JSONField(default=dict)  # storing fontsize, font type, mode
    account_recovery_email = models.EmailField()
    account_recovery_phone = models.CharField(max_length=15)
    account_recovery_question = models.CharField(max_length=255)
    account_recovery_answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
