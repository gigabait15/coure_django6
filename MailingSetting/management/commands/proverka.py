from pprint import pprint
from django.core.management import BaseCommand
from UserService.models import ServiceClient


class Command(BaseCommand):
    """Команда для проверки разрешений у пользователя"""

    def handle(self, *args, **options):
        user = ServiceClient.objects.get(email="admin")
        groups = user.groups.all()
        # Получаем все разрешения для пользователя
        permissions = user.get_all_permissions()
        # Выводим список разрешений
        pprint(groups)
        pprint(permissions)
