from datetime import datetime
from datetime import timedelta

from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail


def send_weekly_digest():
    """Отправляет недельную сводку по новым Постам."""
    Post = apps.get_model("post.Post")
    CategorySubscribers = apps.get_model("post.CategorySubscribers")

    date_from = datetime.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gt=date_from)
    posts_list = [
        post.preview() + f"... Читайте полную версию по ссылке: {settings.SITE_DOMAIN}news/{post.id}"
        for post in new_posts
    ]
    posts_msg = "\n".join(posts_list)
    for post in new_posts:
        categories = post.postcategory_set.all().values_list("category_id", flat=True)
        subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
        for subscriber in subscribers:
            user_email = subscriber.subscriber.email or "test@example.com"
            send_mail(
                f"Недельный дайджест!",
                posts_msg,
                "no-reply@example.com",
                [user_email],
                fail_silently=False,
            )


class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        trigger = CronTrigger(day_of_week="sun", hour='12', minute='0', timezone='Europe/Moscow')
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_weekly_digest, trigger)
        scheduler.start()
