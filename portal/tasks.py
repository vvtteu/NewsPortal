from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber, Post
from datetime import datetime, timedelta
from django.contrib.auth.models import User


@shared_task
def send_notification_email(post_id):
    try:
        post = Post.objects.get(id=post_id)
        subscribers = Subscriber.objects.filter(category__in=post.categories.all())
        
        for subscriber in subscribers:
            send_mail(
                'Новая статья в вашей любимой категории',
                f'Заголовок: {post.title}\nТекст: {post.text[:50]}...\n\n'
                f'Читать полностью: http://127.0.0.1:8000{post.get_absolute_url()}',
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.user.email],
                fail_silently=False,
            )
    except Exception as e:
        return f"Ошибка при отправке уведомлений: {str(e)}"

@shared_task
def send_weekly_newsletter():
    try:
        week_ago = datetime.now() - timedelta(days=7)
        posts = Post.objects.filter(created_at__gte=week_ago)

        users = User.objects.all()
        
        subject = 'Еженедельная рассылка новостей'
        message = 'Последние новости за неделю:\n\n'
        for post in posts:
            message += f"{post.title}\n{post.text[:50]}...\n"
            message += f"Читать полностью: http://127.0.0.1:8000{post.get_absolute_url()}\n\n"

        for user in users:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

    except Exception as e:
        return f"Ошибка при отправке рассылки: {str(e)}"
