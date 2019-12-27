from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TicketList

app_name = 'chat'

urlpatterns = [
    path('ticket/', TicketList.as_view(), name='ticketList'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
