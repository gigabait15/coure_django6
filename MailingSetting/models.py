from django.db import models
from UserService.models import ServiceClient
from django.utils import timezone


NULLABLE = {'blank': True, 'null': True}

class MessageMailing(models.Model):
    letter_subject = models.CharField(max_length=200, verbose_name='тема письма')
    letter_body = models.TextField(verbose_name='тело письма')

    client = models.ForeignKey(ServiceClient, on_delete=models.CASCADE, verbose_name='Клиент сервиса')

    def __str__(self):
        return self.letter_body

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылок'


class MailingSetting(models.Model):
    STATUS_CHOICES = [
        ('создана', 'создана'),
        ('запущена', 'запущена'),
        ('завершена', 'завершена'),
    ]

    PERIODICITY_CHOICES = [
        ('ежедневно', 'daily'),
        ('еженедельно', 'weekly'),
        ('ежемесячно', 'monthly'),
    ]
    first_send_datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата и время первой отправки")
    periodicity = models.CharField(choices=PERIODICITY_CHOICES, default='ежедневно',
                                   max_length=20, verbose_name="Периодичность")
    status = models.CharField(choices=STATUS_CHOICES, default='создана', max_length=20, verbose_name="Статус")
    client = models.ManyToManyField(ServiceClient, verbose_name='Клиент сервиса')
    message = models.OneToOneField(MessageMailing, on_delete=models.CASCADE, verbose_name='Сообщение рассылки')
    created_by = models.ForeignKey(ServiceClient, on_delete=models.CASCADE, related_name='created_mailings',
                                   verbose_name='Создатель рассылки', default=1)

    def __str__(self):
        return f"{self.first_send_datetime}: {self.status}"

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылок'
        permissions = [
            ("can_change_status_mailingsetting", f"Can change status {verbose_name}"),
            (f'can_view_mailingsetting', f'Can view {verbose_name} '),
        ]


class MailingAttempt(models.Model):
    ATTEMPT_CHOICES = [
        ('успешно', 'успешно'),
        ('не успешно', 'не успешно'),
    ]
    last_attempt_datatime = models.CharField(max_length=200, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(choices=ATTEMPT_CHOICES, max_length=200, verbose_name='статус попытки ')
    mail_server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailingsetting = models.ForeignKey(MailingSetting, on_delete=models.CASCADE, verbose_name='настройка рассылки')

    def __str__(self):
        return f"{self.attempt_status} - {self.last_attempt_datatime}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
