from django.contrib import admin

from .models import CannedMessage, Message, Ticket

admin.site.register(CannedMessage)
admin.site.register(Message)
admin.site.register(Ticket)
