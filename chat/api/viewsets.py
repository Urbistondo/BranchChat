from django.contrib.auth import get_user_model
from filters.mixins import FiltersMixin
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from chat.models import CannedMessage, Message, Ticket
from chat.serializers import CannedMessageSerializer, MessageSerializer, TicketSerializer


User = get_user_model()


class TicketViewSet(FiltersMixin, ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('user', 'agent', 'category', 'priority')
    ordering = ('category',)

    filter_mappings = {
        'user': 'user_id',
        'agent': 'agent_id',
        'category': 'category',
        'priority': 'priority',
    }

    filter_value_transformations = {
        'agent': lambda val: val if val != 'null' else None  # cm to ft
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = User.objects.get(id=self.request.data['user_id'])
            serializer.save(user=user)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(ticket=self.kwargs['ticket_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ticket = Ticket.objects.get(id=kwargs['ticket_pk'])
            author = User.objects.get(id=self.request.data['author_id'])
            serializer.save(author=author, ticket=ticket, body=self.request.data['body'])
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CannedMessageViewSet(FiltersMixin, ModelViewSet):
    queryset = CannedMessage.objects.all()
    serializer_class = CannedMessageSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('category', )
    ordering = ('category',)

    filter_mappings = {
        'category': 'category',
    }

    def get_queryset(self):
        if 'category' in self.kwargs:
            return CannedMessage.objects.filter(category=self.kwargs['category'])
        else:
            return CannedMessage.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(category=self.request.data['category'], body=self.request.data['body'])
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
