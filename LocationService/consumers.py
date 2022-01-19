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
#import bus
from core.models import Bus


# class LocationConsumer(AsyncConsumer):
#     data = ''

#     async def websocket_connect(self, event):
#         self.bus = self.scope["url_route"]["kwargs"]["bus"]
#         print(self.bus)
#         #self.user = self.scope["user"]
#         self.bus_room = self.bus

#         await self.channel_layer.group_add(self.bus_room, self.channel_name)

#         await self.send(
#             {
#                 "type": "websocket.accept",
#             }
#         )
#         await self.send(
#             {
#                 "type": "websocket.send",
#                 "text": "connected",
#             }
#         )

#     async def websocket_receive(self, event):
#         # await self.send({
#         #     "type": "websocket.send",
#         #     "text": event["text"],
#         # })
#         # print(event)
#         self.user = self.scope["user"]
#         print(self.user)
#         print(f'{randint(1,100)}{event["text"]}')

#         # if self.user.is_authenticated:
#         await self.channel_layer.group_send(
#             self.bus_room,
#             {
#                 "type": "send_message",
#                 "text": event["text"],
#             },
#         )

#     async def send_message(self, event):
#         # print("message hit")
#         await self.send(
#             {
#                 "type": "websocket.send",
#                 "text": event['text'],
#             }
#         )

#     async def websocket_disconnect(self, event):
#         await self.send({"type": "websocket.send", "text": "Connection close"})
#         await self.send({"type": "websocket.close", "text": "Connection close"})


class LocationConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.token = self.scope["url_route"]["kwargs"]["token"]
        self.bus = self.scope["url_route"]["kwargs"]["bus"]

        print(self.token)
        print(self.bus)
        if self.token is None:
            print('token is none')
        if self.token != 'notoken':
            self.user = await self.check_token(self.token)
            await self.active_status(self.user)

        self.bus_room = self.bus
        # self.channel_name = f'{self.bus}-channel'
        # print('channel name in setconsumer: ', self.channel_name)
        # print('bus name in setconsumer: ', self.bus_room)
        await self.channel_layer.group_add(self.bus_room, self.channel_name)
        await self.send({
            "type": "websocket.accept",

        })

    async def websocket_receive(self, event):
        print(event['text'])
        # await self.send({
        #     "type": "websocket.send",
        #     "text": event["text"]+f'{os.linesep}time: {datetime.datetime.now()}',
        # })

        await self.channel_layer.group_send(
            self.bus_room,
            {
                "type": "send_message",
                "text": event["text"],
            },
        )

    async def websocket_disconnect(self, event):
        await self.send({
            "type": "websocket.send",
            "text": "Connection close"
        })
        await self.send({
            "type": "websocket.close",
            "text": "Connection close"
        })
        if self.token is not None or self.token != '':
            self.user = await self.check_token(self.token)
            await self.active_status(self.user)

    @database_sync_to_async
    def check_token(self, token):
        try:
            token = Token.objects.get(key=token)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()

    @database_sync_to_async
    def active_status(self, user):
        try:
            bus = Bus.objects.get(user=user)
            bus.change_active_status()
        except Bus.DoesNotExist:
            return AnonymousUser()

    async def send_message(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": event["text"],
            }
        )
