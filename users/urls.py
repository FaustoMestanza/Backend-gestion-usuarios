from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RefreshView, MeView, UserViewSet

# 🔹 Router para el CRUD de usuarios
router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')

urlpatterns = [
    path("auth/login/",   LoginView.as_view(),   name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/me/",      MeView.as_view(),      name="auth-me"),
    path("", include(router.urls)),  
]
