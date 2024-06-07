from django.db.models import Count
from django.views import generic
from Blog.models import Blog
from MailingSetting.models import MailingSetting


class BlogListView(generic.ListView):
    """Просмотр статей"""

    model = Blog

    def get_queryset(self):
        """Отображение случайных статей"""
        return Blog.objects.order_by("?")[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем количество всех рассылок
        total_mailings_count = MailingSetting.objects.count()
        # Получаем количество активных рассылок
        active_mailings_count = MailingSetting.objects.filter(status="запущена").count()
        # Получаем количество уникальных клиентов для каждой рассылки
        unique_clients_per_mailing = MailingSetting.objects.annotate(
            number_of_unique_clients=Count("client", distinct=True)
        )
        context["total_mailings_count"] = total_mailings_count
        context["active_mailings_count"] = active_mailings_count
        context["unique_clients_per_mailing"] = unique_clients_per_mailing
        return context


class BlogDetailView(generic.DetailView):
    """Просмотр статьи"""

    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object
