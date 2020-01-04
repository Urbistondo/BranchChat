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

from .models import Message, Ticket
from .serializers import MessageSerializer, TicketSerializer

from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

# API views
# class TicketList(ListCreateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
#
# class TicketDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     lookup_field = 'id'
#
#
# class TicketMessageList(ListAPIView):
#     serializer_class = MessageSerializer
#
#     def get_queryset(self):
#         print('HERE')
#         print(self.request.data)
#         return Ticket.objects.filter(id=self.request.data['id']).message_set.all()
#
#
# def what_is_this_function(request, id):
#     ticket = Ticket.objects.get(id=id)
#     messages = ticket.message_set.all()
#     serializer = MessageSerializer(messages, many=True)
#
#     return JsonResponse(serializer.data, safe=False)


# @csrf_exempt
# def snippet_list(request):
#     if request.method == 'GET':
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)
#
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         print('REQUESSSSSSSSSSST')
#
#         data = JSONParser().parse(request)
#         print(data)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return JsonResponse(serializer.data, status=201)
#
#         return JsonResponse(serializer.errors, status=400)
#
# class MessageDetail(APIView):
#     def get_object(self, id):
#         try:
#             return Message.objects.get(id=id)
#         except Message.DoesNotExist:
#             raise Http404
#
#     def get(self, request, ticket_id):
#         ticket = Ticket.objects.get(id=self.request.data['ticket_id'])
#         messages = Message.objects.all(ticket_id=ticket.id)
#         serializer = MessageSerializer(messages)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class MessageCreateAPIView(CreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#
#     def perform_create(self, serializer):
#         ticket = Ticket.objects.get(id=self.request.data['ticket_id'])
#         serializer.save(author=self.request.user, ticket=ticket)


# class MessageList(APIView):
#     def get_object(self, id):
#         try:
#             return Message.objects.get(id=id)
#         except Message.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id):
#         message = self.get_object(id)
#         serializer = MessageSerializer(message)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         print('BIIIIIITCH')
#         print(request.data)
#         serializer = MessageSerializer(data=request.data)
#         print(serializer.is_valid())
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
