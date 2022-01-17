import asyncio
import datetime
import os
import time
from channels.consumer import SyncConsumer, AsyncConsumer
from random import randint
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.auth import login
# import user model
from django.contrib.auth.models import User
# import annoynomus user
from django.contrib.auth.models import AnonymousUser


class SetLocationConsumer(AsyncConsumer):
    data = ''

    async def websocket_connect(self, event):
        self.bus = self.scope["url_route"]["kwargs"]["bus"]
        print(self.bus)
        self.user = self.scope["user"]
        self.bus_room = self.bus
        await self.channel_layer.group_add(self.bus_room, self.channel_name)

        await self.send(
            {
                "type": "websocket.accept",
            }
        )
        await self.send(
            {
                "type": "websocket.send",
                "text": "connected",
            }
        )

    async def websocket_receive(self, event):
        # await self.send({
        #     "type": "websocket.send",
        #     "text": event["text"],
        # })
        # print(event)
        self.user = self.scope["user"]
        print(self.user)
        print(f'{randint(1,100)}{event["text"]}')

        # if self.user.is_authenticated:
        await self.channel_layer.group_send(
            self.bus_room,
            {
                "type": "send_message",
                "text": event["text"],
            },
        )

    async def send_message(self, event):
        # print("message hit")
        await self.send(
            {
                "type": "websocket.send",
                "text": event["text"],
            }
        )

    async def websocket_disconnect(self, event):
        await self.send({"type": "websocket.send", "text": "Connection close"})
        await self.send({"type": "websocket.close", "text": "Connection close"})


# class LocationConsumer(AsyncConsumer):

#     async def websocket_connect(self, event):
#         # self.bus_room = 'location_group'
#         # await self.channel_layer.group_add(
#         #     self.bus_room,
#         #     self.channel_name
#         # )
#         await self.send({
#             "type": "websocket.accept",
#         })
#         # time.sleep(10)

#     async def websocket_receive(self, event):

#         await self.send({
#             "type": "websocket.send",
#             "text": event["text"]+f'{os.linesep}time: {datetime.datetime.now()}',
#         })

#     async def websocket_disconnect(self, event):
#         await self.send({
#             "type": "websocket.send",
#             "text": "Connection close"
#         })
#         await self.send({
#             "type": "websocket.close",
#             "text": "Connection close"
#         })
