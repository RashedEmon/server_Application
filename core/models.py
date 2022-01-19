from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import Choices
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class Bus(models.Model):

    BUS_TYPE_CHOICES = [
        ("ST", "Student"),
        ("SF", "Staff"),
    ]
    user = models.OneToOneField(
        User, verbose_name="Bus_User", on_delete=models.CASCADE)
    bus_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    bus_name = models.CharField(max_length=50)
    bus_type = models.CharField(
        max_length=10,
        choices=BUS_TYPE_CHOICES,
        default="ST",
    )
    # bus_service_status = models.BooleanField(default=True)
    bus_active_status = models.BooleanField(default=False)
    # bus_created = models.DateTimeField(auto_now=True)
    bus_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bus_name

    def change_active_status(self):
        if self.bus_active_status:
            self.bus_active_status = False
        else:
            self.bus_active_status = True
        self.save()


class Bus_Route(models.Model):
    OFF_DAY_CHOICES = [
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    is_on = models.BooleanField(default=True)
    start_place = models.CharField(max_length=50)
    end_place = models.CharField(max_length=50)
    routes = models.TextField()
    off_day = models.CharField(
        max_length=10, choices=OFF_DAY_CHOICES, default="None")
    departure_time = models.TimeField()

    def __str__(self):
        return self.start_place + " to " + self.end_place


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# def update_is_on(sender, instance, **kwargs):
#     if not instance.is_on:
#         Bus_Route.objects.filter(bus=instance).update(is_on=True)
#     else:
#         Bus_Route.objects.filter(bus=instance).update(is_on=False)
