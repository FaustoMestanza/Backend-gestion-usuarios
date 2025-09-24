from django.urls import path
from .views import LoginView, RefreshView, MeView

urlpatterns = [
    path("auth/login/",   LoginView.as_view(),   name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/me/",      MeView.as_view(),      name="auth-me"),
]
