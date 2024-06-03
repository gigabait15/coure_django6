from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from UserService.forms import UsersRegisterForm, UsersProfileForm
from UserService.models import ServiceClient
from django.core.mail import EmailMessage


class UserServiceListView(PermissionRequiredMixin, ListView):
    """Просмотр списка клиентов"""
    model = ServiceClient
    template_name = 'UserService/userservice_list.html'
    permission_required = 'UserService.can_view_serviceclient'

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = ServiceClient
    form_class = UsersRegisterForm
    template_name = 'UserService/register.html'
    success_url = reverse_lazy('UserService:login')
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(user)
        return HttpResponseRedirect(self.get_success_url())

    def send_activation_email(self, user):
        """Настройка и отправка активационного письма"""
        mail_subject = 'Активируйте вашу учетную запись.'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://127.0.0.1:8000/UserService/activate/{uid}/{token}/"
        message = render_to_string('UserService/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def get_success_url(self):
        return self.success_url


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = ServiceClient.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ServiceClient.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.is_active = True
            user.save()
            link = f'http://127.0.0.1:8000/UserService/'
            return HttpResponse(f'Благодарим вас за подтверждение по электронной почте. '
                                f'Теперь вы можете войти в свой аккаунт.  <a href="{link}">Перейти</a>')
        else:
            return HttpResponse('Ссылка активации недействительна!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Method not allowed', status=405)


class ProfileView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """Профиль пользователя"""
    model = ServiceClient
    form_class = UsersProfileForm
    template_name = 'UserService/userservice_form.html'
    permission_required = 'UserService.can_view_serviceclient'
    success_url = reverse_lazy('UserService:user_list')

    def get_object(self, queryset=None):
        return self.request.user

    def has_permission(self):
        """Проверка на автора публикации """
        if self.request.user == self.request.user:
            return True
        return super().has_permission()

