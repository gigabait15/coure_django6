import os
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from MailingSetting.forms import MailingSettingForm, MailingMessageForm
from MailingSetting.models import MessageMailing, MailingSetting, MailingAttempt
from config import settings


# Generic для Сообщений
class MessageMailingListView(generic.ListView):
    """Просмотр списка сообщений для рассылки"""
    model = MessageMailing

class MessageMailingCreateView(LoginRequiredMixin, generic.CreateView):
    """Создание сообщения для рассылки"""
    model = MessageMailing
    form_class = MailingMessageForm
    template_name = 'MailingSetting/messagemailing_form.html'
    success_url = reverse_lazy('MailingSetting:message_list')

    def form_valid(self, form):
        form.instance.client = self.request.user  # Привязываем текущего пользователя
        return super().form_valid(form)


class MessageMailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """Просмотр сообщения для рассылки"""
    model = MessageMailing
    form_class = MailingMessageForm
    template_name = 'MailingSetting/messagemailing_detail.html'
    success_url = reverse_lazy('MailingSetting:message_list')

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()


class MessageMailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """Изменение сообщения для рассылки"""
    model = MessageMailing
    form_class = MailingMessageForm
    template_name = 'MailingSetting/messagemailing_form.html'
    success_url = reverse_lazy('MailingSetting:message_list')

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()

class MessageMailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Удаление сообщения для рассылки"""
    model = MessageMailing
    success_url = reverse_lazy('MailingSetting:message_list')

    def test_func(self):
        obj = self.get_object()
        return (
                self.request.user == obj.client or
                self.request.user.has_perm('MailingSetting.delete_mailing_setting') or
                self.request.user.is_superuser
        )


# Generic для Настройки сообщений
class SettingStatusLaunchedView(generic.View):
    model = MailingSetting

    def post(self, request, pk):
        object = get_object_or_404(MailingSetting, pk=pk)
        object.status = 'запущена'
        object.save()
        return redirect(reverse('MailingSetting:mailing_list'))

class SettingStatusCompletedView(PermissionRequiredMixin, generic.View):
    model = MailingSetting
    permission_required = 'MailingSetting.can_change_status_mailingsetting'

    def post(self, request, pk):
        object = get_object_or_404(MailingSetting, pk=pk)
        object.status = 'завершена'
        object.save()
        return redirect(reverse('MailingSetting:mailing_list'))


class MailingSettingListView(generic.ListView):
    """Просмотр списка настроек для рассылкок"""
    model = MailingSetting

class MailingSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    """Просмотр одной настройки для рассылки"""
    model = MailingSetting
    form_class = MailingSettingForm
    permission_required = 'MailingSetting.can_view_mailingsetting'

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()


class MailingSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """Создание настройки для рассылки"""
    model = MailingSetting
    form_class = MailingSettingForm
    template_name = 'MailingSetting/mailingsetting_form.html'
    success_url = reverse_lazy('MailingSetting:mailing_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()


class MailingSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = MailingSetting
    form_class = MailingSettingForm
    template_name = 'MailingSetting/mailingsetting_form.html'
    success_url = reverse_lazy('MailingSetting:mailing_list')

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()

    def form_valid(self, form):
        response = super().form_valid(form)
        # Сохраняем выбранных клиентов
        self.object.client.set(form.cleaned_data['client'])
        return response

class MailingSettingDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = MailingSetting
    success_url = reverse_lazy('MailingSetting:mailing_list')

    def test_func(self):
        obj = self.get_object()
        return (
                self.request.user == obj.created_by or
                self.request.user.has_perm('MailingSetting.delete_mailing_setting') or
                self.request.user.is_superuser
        )


# Generic для Сбора отчета отправок
class MailingAttemptListView(generic.ListView):
    """Просмотр логов по рассылке"""
    model = MailingAttempt


class MailingAttemptDetailView(generic.DetailView):
    """Журнал логов планировщика"""
    model = MailingAttempt
    template_name = 'MailingSetting/mailingattempt_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'scheduler.log')

        mailing_attempt = self.get_object()
        mailing_setting = mailing_attempt.mailingsetting

        if mailing_setting:
            log_content = []

            with open(log_file_path, 'r') as file:
                for line in file:
                    # Проверяем точное вхождение id рассылки
                    if f'id {mailing_setting.id}' in line:
                        log_content.append(line.strip())

            context['log_content'] = log_content
        return context