from django import forms
from django.contrib import admin
from MailingSetting.models import MailingSetting, MessageMailing, MailingAttempt


class MailingSettingAdminSuperUserForm(forms.ModelForm):
    class Meta:
        model = MailingSetting
        fields = "__all__"


class MailingSettingAdminManagerForm(forms.ModelForm):
    class Meta:
        model = MailingSetting
        fields = ["status"]


@admin.register(MailingSetting)
class MailingSettingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_send_datetime",
        "periodicity",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("message__letter_subject",)
    filter_horizontal = ("client",)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return MailingSettingAdminSuperUserForm
        return MailingSettingAdminManagerForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ["id", "first_send_datetime", "periodicity"]


class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_attempt_datatime",
        "attempt_status",
    )


admin.site.register(MessageMailing)
admin.site.register(MailingAttempt, MailingAttemptAdmin)
