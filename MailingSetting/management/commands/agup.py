from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """Добавление пользователя в группу с соответствующими разрешениями"""

    def handle(self, *args, **kwargs):
        user_email = "AiMobil@yandex.ru"
        User = get_user_model()

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Пользователь с email {user_email} не найден")
            )
            return

        name = "managers"
        # Получаем или создаем группу managers
        managers_group, created = Group.objects.get_or_create(name=name)

        # Добавляем пользователя в группу managers
        user.groups.add(managers_group)

        # Устанавливаем статус is_staff для пользователя
        user.is_staff = True
        user.save()

        # Разрешения
        permissions = [
            "can_view_serviceclient",
            "view_serviceclient",
            "change_serviceclient",
            "can_change_is_active_serviceclient",
            "can_view_mailingsetting",
            "view_mailingsetting",
            "change_mailingsetting",
            "can_change_status_mailingsetting",
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                managers_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Разрешение {perm} не найдено"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Пользователь {user_email} "
                f"добавлен в группу {name} с необходимыми разрешениями"
            )
        )
