from rest_framework_nested import routers

from chat.api.viewsets import MessageViewSet, TicketViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register('tickets', TicketViewSet, basename='ticket')

tickets_router = routers.NestedSimpleRouter(router, 'tickets', lookup='ticket')
tickets_router.register('messages', MessageViewSet)
