from django.urls import path
from django.views.decorators.cache import cache_page
from MailingSetting.apps import MailingSettingConfig
from MailingSetting.views import (
    MessageMailingListView,
    MessageMailingCreateView,
    MailingSettingListView,
    MailingSettingDetailView,
    MailingSettingCreateView,
    MailingAttemptListView,
    SettingStatusLaunchedView,
    SettingStatusCompletedView,
    MailingAttemptDetailView,
    MailingSettingUpdateView,
    MailingSettingDeleteView,
    MessageMailingDetailView,
    MessageMailingUpdateView,
    MessageMailingDeleteView,
)


app_name = MailingSettingConfig.name


urlpatterns = [
    # урлы для сообщений
    path("", cache_page(60)(MessageMailingListView.as_view()), name="message_list"),
    path("message_create/", MessageMailingCreateView.as_view(), name="message_create"),
    path(
        "message_detail/<int:pk>/",
        MessageMailingDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "message_update/<int:pk>/",
        MessageMailingUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message_delete/<int:pk>/",
        MessageMailingDeleteView.as_view(),
        name="message_delete",
    ),
    # урлы для настройки рассылок
    path(
        "mailing_launched/<int:pk>/",
        SettingStatusLaunchedView.as_view(),
        name="mailing_launched",
    ),
    path(
        "mailing_completed/<int:pk>/",
        SettingStatusCompletedView.as_view(),
        name="mailing_completed",
    ),
    path(
        "mailing_list/",
        cache_page(60)(MailingSettingListView.as_view()),
        name="mailing_list",
    ),
    path(
        "mailing_detail/<int:pk>/",
        MailingSettingDetailView.as_view(),
        name="mailing_detail",
    ),
    path(
        "mailing_update/<int:pk>/",
        MailingSettingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing_delete/<int:pk>/",
        MailingSettingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailing_create/", MailingSettingCreateView.as_view(), name="mailing_create"),
    # урлы для логов рассылок
    path("attempt/", MailingAttemptListView.as_view(), name="attempt"),
    path(
        "logs_scheduler/<int:pk>/",
        MailingAttemptDetailView.as_view(),
        name="logs_scheduler",
    ),
]
