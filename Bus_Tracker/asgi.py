"""
ASGI config for Bus_Tracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bus_Tracker.settings')

# application = get_asgi_application()

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# import SessionMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from core import views
import core
from LocationService.consumers import SetLocationConsumer, LocationConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


application = ProtocolTypeRouter(
    {
        # Django's ASGI application to handle traditional HTTP requests
        # WebSocket chat handler
        "websocket": SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        url(r"^ws/location/(?P<bus>\w+)$", SetLocationConsumer),
                        url(r"^ws/getlocation/$", LocationConsumer),
                    ]
                )
            )
        ),
    }
)
