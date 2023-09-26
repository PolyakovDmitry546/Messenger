import json
from abc import ABC, abstractmethod

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Channel, ChannelMessage, Dialog, DialogMessage, Message
from .serializers import ChannelMessageSerializer, DialogMessageSerializer


class ChatConsumer(ABC, AsyncWebsocketConsumer):
    @abstractmethod
    def make_room_group_name(self):
        self.room_group_name = None

    @abstractmethod
    async def make_message_owner(self):
        self.message_owner = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.make_room_group_name()
        await self.make_message_owner()
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @abstractmethod
    def create_message(self, message_text) -> Message:
        pass

    @abstractmethod
    def serialize_message(self, message):
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]["text"]

        message = self.create_message(message_text)
        await message.asave()

        serializer = self.serialize_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": serializer.data},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ChannelConsumer(ChatConsumer):
    def make_room_group_name(self):
        self.room_group_name = "channel_%s" % self.room_name

    async def make_message_owner(self):
        self.message_owner = await Channel.objects.aget(pk=self.room_name)

    def create_message(self, message_text) -> Message:
        return ChannelMessage(author=self.user, text=message_text, owner=self.message_owner)

    def serialize_message(self, message):
        return ChannelMessageSerializer(message)


class DialogConsumer(ChatConsumer):
    def make_room_group_name(self):
        self.room_group_name = "dialog_%s" % self.room_name

    async def make_message_owner(self):
        self.message_owner = await Dialog.objects.aget(pk=self.room_name)

    def create_message(self, message_text) -> Message:
        return DialogMessage(author=self.user, text=message_text, owner=self.message_owner)

    def serialize_message(self, message):
        return DialogMessageSerializer(message)
