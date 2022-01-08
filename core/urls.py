from django.contrib import admin
from django.urls import path, include
from . import views
import api

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginView, name="login"),
    path("api", include("api.urls"), name="api"),
]
