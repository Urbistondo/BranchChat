from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
import json

from .models import Message, Ticket
from .serializers import MessageSerializer


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }

        self.send_chat_message(content)

    def new_message(self, data):
        serializer = MessageSerializer(data=data['message'])
        if serializer.is_valid(raise_exception=True):
            ticket = Ticket.objects.get(id=data['message']['ticket_id'])
            author = User.objects.get(id=data['message']['author_id'])
            message = serializer.save(author=author, ticket=ticket, body=data['message']['body'])

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    @staticmethod
    def message_to_json(message):
        return {
            'ticket_id': message.ticket_id,
            'author_id': message.author_id,
            'body': message.body,
            'sent_at': message.sent_at,
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        # Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        # Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
        # Group names may only contain letters, digits, hyphens, and periods. Therefore this example code will fail on room names that have other characters.
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
