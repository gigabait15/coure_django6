import os
import schedule
import time
import logging
from django.core.management import BaseCommand
from config import settings
from .send_mail import send_mail
from MailingSetting.models import MailingSetting
from django.utils import timezone


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(settings.BASE_DIR, 'logs', 'scheduler.log'))
logger = logging.getLogger()

class Command(BaseCommand):
    """Команда для планировщика"""
    tasks = {}

    def handle(self, *args, **kwargs):
        """Запуск планировщика"""
        self.restore_tasks()
        while True:
            self.update_tasks()
            schedule.run_pending()
            time.sleep(360)

    def restore_tasks(self):
        """Проверка на статус рассылки"""
        items = MailingSetting.objects.filter(status='запущена')
        for setting in items:
            if setting.id not in self.tasks:
                self.schedule_job(setting)

    def update_tasks(self):
        """Обновление задач """
        items = MailingSetting.objects.all()
        for setting in items:
            if setting.status == 'запущена' and setting.id not in self.tasks:
                self.schedule_job(setting)
            elif setting.status != 'запущена' and setting.id in self.tasks:
                logger.info(f"Отмена запланированной отправки письма "
                            f"для настройки с id {setting.id}")
                schedule.cancel_job(self.tasks[setting.id])
                del self.tasks[setting.id]

    def schedule_job(self, setting):
        """Запись в словарь планировщика данных о рассылке для запуска"""
        local_tz = timezone.get_current_timezone()
        send_time = setting.first_send_datetime.astimezone(local_tz).strftime("%H:%M")
        periodicity = setting.periodicity
        job = None

        try:
            if periodicity == 'ежедневно':
                job = schedule.every().day.at(send_time).do(send_mail, id=setting.id)
                logger.info(f"Ежедневная задача запланирована для настройки с id {setting.id}")
            elif periodicity == 'еженедельно':
                job = schedule.every(7).days.at(send_time).do(send_mail, id=setting.id)
                logger.info(f"Еженедельная задача запланирована для настройки с id {setting.id}")
            elif periodicity == 'ежемесячно':
                job = schedule.every(30).days.at(send_time).do(send_mail, id=setting.id)
                logger.info(f"Ежемесячная задача запланирована для настройки с id {setting.id}")

            if job:
                self.tasks[setting.id] = job
                logger.info(f"Следующая отправка письма для настройки с id {setting.id} запланирована на {job.next_run}")
            else:
                logger.warning(f"Не удалось запланировать задачу для настройки с id {setting.id}")
        except Exception as e:
            logger.error(f"Ошибка при планировании задачи для настройки с id {setting.id}: {e}")
