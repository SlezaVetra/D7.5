from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views import View


class JoinAuthorView(LoginRequiredMixin, View):
    """Представление для добавления Пользователя к Авторам."""
    def get(self, request, *args, **kwargs):
        """Добавляет пользователя к Авторам."""
        Author = apps.get_model("author.Author")
        user = request.user
        with transaction.atomic():
            author, created = Author.objects.get_or_create(user=user)
            if created:
                Group = apps.get_model("auth.Group")
                author_group = Group.objects.get(name=settings.AUTHORS_GROUP)
                user.groups.add(author_group)
        return redirect("/news/")
