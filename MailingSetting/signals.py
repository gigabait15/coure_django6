from django.db.models.signals import post_save
from django.dispatch import receiver
from MailingSetting.models import MailingSetting


@receiver(post_save, sender=MailingSetting)
def send_email_on_status_change(sender, instance, created, **kwargs):
    """Проверка на запуск рассылки для отправки письма и запуска расслыки"""
    if instance.status == "запущена" and not created:
        # Отправить сообщение
        from django.core.management import call_command

        call_command("send_mail", instance.id)
