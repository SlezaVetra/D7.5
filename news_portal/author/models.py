from allauth.account.signals import user_signed_up
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# cвязь «один к одному» с встроенной моделью пользователей User;
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.


class Author(models.Model):
    """Модель авторов статей."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=False, blank=False, default=0)

    def update_rating(self, user):
        """
        Обновляет рейтинг пользователя.
        Он состоит из следующего:
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора.
        """
        authors = Author.objects.filter(user=user)
        if not authors.exists():
            return

        author = authors.first()
        posts_rating = 0
        post_comments_rating = 0
        for post in author.posts.all():
            posts_rating += post.rating * 3
            post_comments_rating += sum(post.comments.all().values_list("rating", flat=True))

        comments_rating = sum(author.user.comments.all().values_list("rating", flat=True))
        self.rating = posts_rating + post_comments_rating + comments_rating
        self.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_local_user_common_group(sender, **kwargs):
    """Добавляет нового локального пользователя в common группу."""
    Group = apps.get_model("auth.Group")
    common_group = Group.objects.get(name=settings.COMMON_GROUP)
    user = kwargs["instance"]
    user.groups.add(common_group)

    user_email = user.email or "test@example.com"
    send_mail(
        f"Hello there!",
        f"Добро пожаловать {user.username}",
        "no-reply@example.com",
        [user_email],
        fail_silently=False,
    )

    return


@receiver(user_signed_up)
def add_user_common_group(sender, **kwargs):
    """Добавляет нового пользователя в common группу."""
    Group = apps.get_model("auth.Group")
    common_group = Group.objects.get(name=settings.COMMON_GROUP)
    user = kwargs["user"]
    user.groups.add(common_group)
    return
