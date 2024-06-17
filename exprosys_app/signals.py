from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from user_agents import parse
from .models import UserSession

@receiver(post_save, sender=User)
def create_user_session(sender, instance, created, **kwargs):
    if not created:
        return

    request = kwargs.get('request')
    if request:
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        device = f"{user_agent.device.family} {user_agent.device.brand} {user_agent.device.model}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        operating_system = f"{user_agent.os.family} {user_agent.os.version_string}"
        location = request.META.get('REMOTE_ADDR')

        refresh = RefreshToken.for_user(instance)
        session_token = str(refresh.access_token)

        UserSession.objects.create(
            user=instance,
            device=device,
            location=location,
            browser=browser,
            operating_system=operating_system,
            session_token=session_token,
            time_of_entry=timezone.now()
        )
