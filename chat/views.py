from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

import json

from .models import CannedMessage, Ticket
from .serializers import CannedMessageSerializer, TicketSerializer

from django.shortcuts import render


User = get_user_model()


def index(request):
    return render(request, 'chat/index.html', {})


def dashboard(request):
    agent = request.user
    tickets = Ticket.objects.filter(agent_id=agent.id)
    if tickets:
        serializedTickets = TicketSerializer(tickets, many=True).data[:]
    else:
        serializedTickets = []

    context = {
        'agent_first_name': agent.first_name,
        'agent_last_name': agent.last_name,
        'tickets': serializedTickets,
    }

    return render(request, 'chat/ticket_home.html', context)


def ticket_view(request, ticket_id):
    agent = request.user
    ticket = Ticket.objects.get(id=ticket_id)
    user = User.objects.get(id=ticket.user_id)
    tickets = Ticket.objects.filter(agent_id=agent.id)
    serialized_tickets = TicketSerializer(tickets, many=True).data[:] if tickets else []
    canned_messages = CannedMessage.objects.all()
    serialized_canned_messages = CannedMessageSerializer(canned_messages, many=True).data[:] if canned_messages else []

    context = {
        'agent_first_name': agent.first_name,
        'agent_last_name': agent.last_name,
        'tickets': serialized_tickets,
        'canned_messages': serialized_canned_messages,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'ticket_id': mark_safe(json.dumps(ticket_id)),
    }

    return render(request, 'chat/ticket.html', context)
