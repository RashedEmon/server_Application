from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import Choices
import uuid

# Create your models here.


class Bus(models.Model):

    BUS_TYPE_CHOICES = [
        ('ST', 'Student'),
        ('SF', 'Staff'),
    ]
    user = models.OneToOneField(
        User, verbose_name="Bus_User", on_delete=models.CASCADE)
    bus_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus_name = models.CharField(max_length=50)
    bus_type = models.CharField(
        max_length=10,
        choices=BUS_TYPE_CHOICES,
        default='ST',
    )
    # bus_service_status = models.BooleanField(default=True)
    bus_active_status = models.BooleanField(default=False)
    #bus_created = models.DateTimeField(auto_now=True)
    bus_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bus_name


class Bus_Route(models.Model):
    OFF_DAY_CHOICES = [
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    start_place = models.CharField(max_length=50)
    end_place = models.CharField(max_length=50)
    routes = models.TextField()
    off_day = models.CharField(
        max_length=10, choices=OFF_DAY_CHOICES, default='None')
    departure_time = models.TimeField()

    def __str__(self):
        return self.start_place + ' to ' + self.end_place
