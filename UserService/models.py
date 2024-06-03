from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class ServiceClient(User):
    email_client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='email',
                                     related_name='client_service_clients', null=True)
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    email_verified = models.BooleanField(default=False, verbose_name='верификация email')

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Cервис клиент'
        verbose_name_plural = 'Cервис клиенты'
        permissions = [
            (f"can_change_is_active_serviceclient", f"Can change is_active status {verbose_name}"),
            (f"can_view_serviceclient", f"Can view {verbose_name}"),
        ]
