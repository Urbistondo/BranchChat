from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TicketDetail, TicketList

app_name = 'chat'

urlpatterns = [
    path('ticket', TicketList.as_view(), name='ticket_list'),
    path('ticket/<str:id>', TicketDetail.as_view(), name='ticket_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
