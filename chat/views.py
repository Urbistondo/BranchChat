from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Ticket
from .serializers import TicketSerializer


# API views
class TicketList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDetail(RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'id'
