import json
import os
from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from django.conf import settings


class Command(BaseCommand):
    """Сохранение данных групп и разрешений в фикстуру"""

    def handle(self, *args, **kwargs):
        # Извлечение данных групп и разрешений
        groups_data = []
        for group in Group.objects.all():
            permissions = [perm.codename for perm in group.permissions.all()]
            groups_data.append({"name": group.name, "permissions": permissions})

        # Определение пути для сохранения фикстуры
        file_path = os.path.join(settings.BASE_DIR, "fixtures", "groups.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Сохранение данных в JSON файл
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(groups_data, file, ensure_ascii=False, indent=4)

        self.stdout.write(
            self.style.SUCCESS("Данные групп и разрешений успешно сохранены в фикстуру")
        )
