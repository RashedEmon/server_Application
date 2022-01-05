from django.contrib import admin
from .models import *
# Register your models here.


class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_id','bus_name', 'bus_type', 'bus_active_status',
                    'bus_last_updated', 'user')
    list_filter = ('bus_type', 'bus_active_status', 'user')
    search_fields = ('bus_name', 'bus_type', 'user')

    class Meta:
        model = Bus


admin.site.register(Bus, BusAdmin)


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('bus', 'start_place', 'end_place',
                    'departure_time', 'off_day', 'routes')
    list_filter = ('bus', 'start_place', 'end_place',
                   'departure_time', 'off_day')
    search_fields = ('bus', 'start_place', 'end_place', 'departure_time')

    class Meta:
        model = Bus_Route


admin.site.register(Bus_Route, BusRouteAdmin)
