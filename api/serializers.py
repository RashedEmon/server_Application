from rest_framework import serializers
from core.models import Bus, Bus_Route


class BusSerializer(serializers.Serializer):
    bus_id = serializers.UUIDField(read_only=True)
    bus_name = serializers.CharField(max_length=50)
    bus_type = serializers.CharField(max_length=10)
    bus_active_status = serializers.BooleanField(read_only=True)
    source = serializers.CharField(max_length=50)
    destination = serializers.CharField(max_length=50)
    departureTime = serializers.TimeField()
    is_on = serializers.BooleanField(read_only=True)
    routes = serializers.CharField(max_length=2000)


class BusDetailsView(serializers.Serializer):

    bus_name = serializers.CharField(max_length=50)
    bus_type = serializers.CharField(max_length=10)
    source = serializers.CharField(max_length=50)
    destination = serializers.CharField(max_length=50)
    departureTime = serializers.TimeField()
    routes = serializers.CharField(max_length=2000)
