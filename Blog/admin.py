# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "image",
        "number_of_views",
        "date_of_publication",
    )
    list_filter = (
        "title",
        "number_of_views",
        "date_of_publication",
    )
    search_fields = ("title",)
    # Исключаем данные поля при создании и редактировании
    readonly_fields = (
        "number_of_views",
        "date_of_publication",
    )

    def get_fields(self, request, obj=None):
        """Возвращает поля при просмотре в админ панели"""
        fields = ["title", "content", "image"]
        if obj:
            fields.append("number_of_views")
            fields.append("date_of_publication")
        return fields
