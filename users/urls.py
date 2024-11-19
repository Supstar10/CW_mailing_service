from django.urls import path
from users.apps import UsersConfig
from .views import UserLoginView, UserLogoutView, UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
]
