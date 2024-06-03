from django.core.management import BaseCommand
from UserService.models import ServiceClient


class Command(BaseCommand):
    """Команда для создание нового пользователя(здесь создание админа)"""

    def handle(self, *args, **options):
        user = ServiceClient.objects.create(
            email='admin',
            full_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('1234')
        user.save()
