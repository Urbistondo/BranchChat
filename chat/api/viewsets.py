from django.contrib.auth import get_user_model
from filters.mixins import FiltersMixin
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from chat.models import Message, Ticket
from chat.serializers import MessageSerializer, TicketSerializer


class TicketViewSet(FiltersMixin, ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('agent', 'category', 'priority')
    ordering = ('category',)

    # add a mapping of query_params to db_columns(queries)
    filter_mappings = {
        'agent': 'agent_id',
        'category': 'category',
        'priority': 'priority',
    }

    filter_value_transformations = {
        'agent': lambda val: val if val != 'null' else None  # cm to ft
    }


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(ticket=self.kwargs['ticket_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ticket = Ticket.objects.get(id=kwargs['ticket_pk'])
            author = get_user_model().objects.get(id=self.request.data['author_id'])
            serializer.save(author=author, ticket=ticket, body=self.request.data['body'])
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
