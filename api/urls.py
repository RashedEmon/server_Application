from django.urls import path, include
from .views import SearchView, BusDetailsView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("search/<str:source>/<str:destination>/", SearchView, name="search"),
    path("details/<uuid:id>/", BusDetailsView, name="bus_details"),
    path("login", obtain_auth_token, name="login"),
]
