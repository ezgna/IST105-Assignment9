from django.urls import path
from . import views

urlpatterns = [
    path("auth/", views.auth_view, name="auth"),
    path("devices/", views.devices_view, name="devices"),
    path("interfaces/", views.interfaces_view, name="interfaces"),
]