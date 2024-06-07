from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ServiceClient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True, verbose_name="комментарий")
    email_verified = models.BooleanField(default=False, verbose_name="верификация email")

    def __str__(self):
        return f"{self.full_name} - {self.user.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
