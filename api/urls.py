from django.urls import path, include
from .views import SearchView, BusDetailsView

urlpatterns = [
    path("search/<str:source>/<str:destination>/", SearchView, name="search"),
    path("details/<uuid:id>/", BusDetailsView, name="bus_details"),
]
