from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Управляющая команда для создания групп пользователей."""

    def handle(self, *args, **options):
        """Создает группы пользователей."""
        Group = apps.get_model("auth.Group")
        Permission = apps.get_model("auth.Permission")

        for group_name, group_perms in settings.GROUP_PERMS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            print(f"Выполнено для {group_name}")
            if created:
                group.permissions.add(*Permission.objects.filter(codename__in=group_perms))
                print(f"Создана группа '{group_name}' с разрешениями: {group_perms}")

