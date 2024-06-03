import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    """Комманда для очистки файла логов"""

    def handle(self, *args, **kwargs):
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'scheduler.log')
        with open(log_file_path, 'w') as file:
            file.write('')
            self.stdout.write(self.style.SUCCESS('файл журнала планировщика очищен.'))

