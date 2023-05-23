import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from django.core.mail import EmailMessage

import uuid
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user']
        self.receiver_id = await sync_to_async(self.scope['url_route']['kwargs'].get)('receiver_id')
        #self.room_group_name = f'chat_{self.sender.id}_{self.receiver_id}'
        self.room_group_name = str(uuid.uuid4())  # Generate a random room name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

     # sending emails

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)

        # Save the message in the database
        message = await sync_to_async(Message.objects.create)(
            sender=self.sender,
            receiver=receiver,
            text=message_text
        )
        room_link = f'http://127.0.0.1:8000/chat/{self.room_group_name}/{self.sender.id}/'
        email_subject = f'New message from {self.sender.username}'
        email_body = f'You have received a new message from {self.sender.username}:\n\n{message_text}. Kindly go to <a href="{room_link}">Reply to message</a>'
        email = EmailMessage(email_subject, email_body, to=[receiver.email])
        await sync_to_async(email.send)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message_text}
        )

        # Send email notification to the receiver
        email_subject = f'New message from {self.sender.username}'
        email_body = f'You have received a new message from {self.sender.username}:\n\n{message_text}'
        email = EmailMessage(email_subject, email_body, to=[receiver.email])
        await sync_to_async(email.send)()

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

""""
 async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)

        # Save the message in the database
        message = await sync_to_async(Message.objects.create)(
            sender=self.sender,
            receiver=receiver,
            text=message_text
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message_text}
        )"""
