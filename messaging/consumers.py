import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user']
        self.receiver_id = await sync_to_async(self.scope['url_route']['kwargs'].get)('receiver_id')
        self.room_group_name = f'chat_{self.sender.id}_{self.receiver_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Create a conversation or retrieve an existing one
        conversation, created = await sync_to_async(Conversation.objects.get_or_create)(participants=self.sender)
        participants = await sync_to_async(conversation.participants.all)()
        if self.receiver_id not in participants.values_list('id', flat=True):
            receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
            await sync_to_async(conversation.participants.set)(list(participants) + [receiver])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # Save the message in the database
        conversation = await sync_to_async(Conversation.objects.get)(participants=self.sender)
        receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
        message = await sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=self.sender,
            recipient=receiver,
            text=message_text
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message_text}
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))


'''# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
'''
