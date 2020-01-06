from rest_framework_nested import routers

from chat.api.viewsets import CannedMessageViewSet, MessageViewSet, TicketViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register('tickets', TicketViewSet, basename='ticket')

tickets_router = routers.NestedSimpleRouter(router, 'tickets', lookup='ticket')
tickets_router.register('messages', MessageViewSet)

canned_message_router = routers.SimpleRouter(trailing_slash=False)
canned_message_router.register('canned_messages', CannedMessageViewSet, basename='canned_message')
