# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from django.apps import AppConfig
import threading


class SchedulerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler_app'

    def ready(self):
        from MailingSetting.management.commands.scheduler import Command

        # Функцию для запуска сервера Redis
        def start_redis_server():
            try:
                # Запуск redis-server
                process = Popen(['redis-server'], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()

                if process.returncode == 1:
                    print('Сервер Redis успешно запущен')
                else:
                    print(f'Не удалось запустить сервер Redis: {stderr.decode()}')
            except Exception as e:
                print(f'Ошибка при запуске сервера Redis: {e}')

        # Запуск сервера Redis в отдельном потоке
        redis_thread = threading.Thread(target=start_redis_server)
        redis_thread.daemon = True
        redis_thread.start()

        # Запуск планировщика
        scheduler_thread = threading.Thread(target=Command().handle)
        scheduler_thread.daemon = True
        scheduler_thread.start()
