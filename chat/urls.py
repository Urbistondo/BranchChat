from django.urls import include, path

from chat.api.router import canned_message_router, router, tickets_router
from .views import dashboard, index, ticket_view
# from .views import MessageCreateAPIView, MessageDetail, TicketDetail, TicketList, TicketMessageList

app_name = 'chat'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<str:ticket_id>', ticket_view, name='ticket_view'),
    path('api/chat/', include(router.urls)),
    path('api/chat/', include(tickets_router.urls)),
    path('api/chat/', include(canned_message_router.urls)),
    # path('tickets', TicketList.as_view(), name='tickets_list'),
    # path('tickets/<str:id>', TicketDetail.as_view(), name='tickets_detail'),
    # path('tickets/<str:id>/messages', TicketMessageList.as_view(), name='tickets_messages'),
    # path('messages', MessageCreateAPIView.as_view(), name='messages_list'),
    # path('messages/<str:id>', MessageDetail.as_view(), name='message_detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
