from django.core.management.base import BaseCommand
from subprocess import Popen, PIPE


class Command(BaseCommand):
    help = 'Start the Redis server'

    def handle(self, *args, **kwargs):
        try:
            # Запускаем redis-server
            process = Popen(['redis-server'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS(
                    'Redis server started successfully'))
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to start Redis server: {stderr.decode()}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error starting Redis server: {e}'))
