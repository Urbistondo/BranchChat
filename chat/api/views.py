from django.http import Http404, JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

import json

from chat.models import Message, Ticket
from chat.serializers import MessageSerializer, TicketSerializer

from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def search_tickets(request, ticket_id):
    return render(request, 'chat/ticket.html', {
        'ticket_id_json': mark_safe(json.dumps(ticket_id))
    })
