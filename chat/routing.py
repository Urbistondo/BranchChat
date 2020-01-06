from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:ticket_id>/', consumers.ChatConsumer),
]
