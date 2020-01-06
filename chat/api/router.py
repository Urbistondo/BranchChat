from rest_framework_nested import routers

from chat.api.viewsets import CannedMessageViewSet, MessageViewSet, TicketViewSet


ticket_router = routers.SimpleRouter(trailing_slash=False)
ticket_router.register('tickets', TicketViewSet, basename='ticket')

message_router = routers.NestedSimpleRouter(ticket_router, 'tickets', lookup='ticket')
message_router.register('messages', MessageViewSet)

canned_message_router = routers.SimpleRouter(trailing_slash=False)
canned_message_router.register('canned_messages', CannedMessageViewSet, basename='canned_message')
