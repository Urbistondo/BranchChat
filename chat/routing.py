from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>[0-9a-f-]+)/$', consumers.ChatConsumer),
    path('ws/<str:ticket_id>/', consumers.ChatConsumer),
]
