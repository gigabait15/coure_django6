from django.urls import path
from django.views.decorators.cache import cache_page
from Blog.apps import BlogConfig
from Blog.views import BlogListView, BlogDetailView


app_name = BlogConfig.name


urlpatterns = [
    path('blog_list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]