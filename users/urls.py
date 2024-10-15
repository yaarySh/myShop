from django.urls import path
from .views import login, logout, register_user, user_detail

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),  # Add the logout URL
    path("me/", user_detail, name="user_detail"),  # Add this line
]
