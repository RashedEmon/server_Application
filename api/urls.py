from django.urls import path, include
from .views import SearchView, BusDetailsView, bus_from_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("search/<str:source>/<str:destination>/", SearchView, name="search"),
    path("details/<uuid:id>/", BusDetailsView, name="bus_details"),
    path("login", csrf_exempt(obtain_auth_token), name="login"),
    path("bus/", bus_from_token, name="bus_from_token"),
]
