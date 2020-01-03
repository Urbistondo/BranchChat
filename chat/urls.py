from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .router import router, tickets_router
# from .views import MessageCreateAPIView, MessageDetail, TicketDetail, TicketList, TicketMessageList

app_name = 'chat'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tickets_router.urls)),
    # path('tickets', TicketList.as_view(), name='tickets_list'),
    # path('tickets/<str:id>', TicketDetail.as_view(), name='tickets_detail'),
    # path('tickets/<str:id>/messages', TicketMessageList.as_view(), name='tickets_messages'),
    # path('messages', MessageCreateAPIView.as_view(), name='messages_list'),
    # path('messages/<str:id>', MessageDetail.as_view(), name='message_detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
