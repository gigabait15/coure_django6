import logging
from django.utils import timezone
from django.core.mail import send_mail
from django.core.management import BaseCommand
from MailingSetting.models import MailingSetting, MailingAttempt
from config import settings

# Настройка логирования
logger = logging.getLogger()

class Command(BaseCommand):
    """Команда для отправки письма и запись в модель 'Попытка рассылки'"""

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID настройки рассылки')

    def handle(self, *args, **kwargs):
        id = kwargs['id']
        now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            setting = MailingSetting.objects.get(id=id)
        except MailingSetting.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Настройка рассылки с ID {id} не найдена"))
            return

        for client in setting.client.all():
            attempt_status = 'успешно'
            mail_server_response = f"Письмо '{setting.message.letter_subject}' успешно отправлено"
            try:
                send_mail(
                    recipient_list=[client.email],
                    subject=setting.message.letter_subject,
                    message=setting.message.letter_body,
                    from_email=settings.DEFAULT_FROM_EMAIL
                )
                logger.info(mail_server_response)
            except Exception as e:
                attempt_status = 'не успешно'
                mail_server_response = f'Ошибка отправки письма: {e}'
                logger.error(mail_server_response)

            mailing_attempt, created = MailingAttempt.objects.get_or_create(
                mailingsetting=setting,
                defaults={
                    'last_attempt_datatime': now,
                    'attempt_status': attempt_status,
                    'mail_server_response': mail_server_response,
                }
            )

            if not created:
                mailing_attempt.last_attempt_datatime = now
                mailing_attempt.attempt_status = attempt_status
                mailing_attempt.mail_server_response = mail_server_response
                mailing_attempt.save()

        self.stdout.write(self.style.SUCCESS(f"Попытка отправки писем для настройки с ID {id} завершена"))
