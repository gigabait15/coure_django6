# Generated by Django 5.0.6 on 2024-06-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="заголовок")),
                ("content", models.TextField(verbose_name="содержимое статьи")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "number_of_views",
                    models.IntegerField(
                        default=0, verbose_name="количество просмотров"
                    ),
                ),
                (
                    "date_of_publication",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата публикации"
                    ),
                ),
            ],
        ),
    ]
