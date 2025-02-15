from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Subscriber
from .tasks import send_notification_email


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_notification_email.delay(instance.id)
