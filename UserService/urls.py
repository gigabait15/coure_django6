from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from UserService.apps import UserServiceConfig
from UserService.views import RegisterView, ProfileView, ActivateView, UserServiceListView

app_name = UserServiceConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='UserService/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_list/', UserServiceListView.as_view(), name='user_list'),

    path('activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),

]