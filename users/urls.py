from django.urls import path
from django.views.generic import TemplateView
from users.apps import UsersConfig
from .views import UserLoginView, UserLogoutView, UserCreateView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email_verification/<str:token>/', email_verification, name='email_verification'),  # Исправлено
]