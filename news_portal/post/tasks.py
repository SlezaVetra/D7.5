from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

from news_portal import celery_app


@celery_app.task
def send_new_post_notification(post_instance_id, categories):
    CategorySubscribers = apps.get_model("post.CategorySubscribers")
    Post = apps.get_model("post.Post")

    post_instance = Post.objects.get(id=post_instance_id)
    subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
    for subscriber in subscribers:
        user_email = subscriber.subscriber.email or "test@example.com"
        send_mail(
            f"Новая запись в вашей подписке по катеогрии {{ subscriber.category.name }}",
            (
                f"{post_instance.preview()}... "
                f"Читайте полную версию по ссылке: {settings.SITE_DOMAIN}news/{post_instance.id}"
            ),
            "no-reply@example.com",
            [user_email],
            fail_silently=False,
        )


@celery_app.task
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
