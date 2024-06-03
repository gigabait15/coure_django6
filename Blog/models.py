from django.db import models

from MailingSetting.models import MailingSetting

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_of_publication = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f"{self.title}"

    class Mate:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'