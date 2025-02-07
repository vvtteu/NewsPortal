from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Subscriber

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscriber.objects.filter(category__in=instance.categories.all())
        for subscriber in subscribers:
            send_mail(
                'Новая статья в вашей любимой категории',
                f'Заголовок: {instance.title}\nТекст: {instance.text[:50]}',
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.user.email],
                fail_silently=False,
            )
