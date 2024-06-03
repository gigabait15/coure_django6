from django.apps import AppConfig


class MailingSettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MailingSetting'

    def ready(self):
        import MailingSetting.signals