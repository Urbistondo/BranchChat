from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
import json

from .models import Message, Ticket
from .serializers import MessageSerializer


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        ticket = Ticket.objects.get(id=data['data']['ticket_id'])
        messages = ticket.message_set.all().order_by('-sent_at')[:10]
        content = {
            'messages': self.messages_to_json(messages),
            'command': 'messages'
        }
        self.send_message(content)

    def new_message(self, data):
        serializer = MessageSerializer(data=data['message'])
        if serializer.is_valid(raise_exception=True):
            ticket = Ticket.objects.get(id=data['message']['ticket_id'])
            author = User.objects.get(id=data['message']['author_id'])
            message = serializer.save(author=author, ticket=ticket, body=data['message']['body'])

            # content = {
            #     'messages': [self.message_to_json(message)],
            #     'command': 'new_message'
            # }

            self.send_chat_message(self.message_to_json(message))
            # self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    @staticmethod
    def message_to_json(message):
        return {
            'ticket_id': str(message.ticket_id),
            'author_id': message.author_id,
            'body': message.body,
            'sent_at': str(message.sent_at),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        # Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        # Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.
        # Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
        # Group names may only contain letters, digits, hyphens, and periods. Therefore this example code will fail on room names that have other characters.
        self.ticket_id = 'chat_%s' % self.scope['url_route']['kwargs']['ticket_id']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.ticket_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.ticket_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.ticket_id,
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
        content = {
            'messages': [message],
            'command': 'new_message'
        }

        # Send message to WebSocket
        self.send(text_data=json.dumps(content))
