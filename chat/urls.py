from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from chat.api.router import canned_message_router, message_router, ticket_router
from .views import dashboard, ticket_view

app_name = 'chat'

schema_view = get_schema_view(
   openapi.Info(
      title="Chat API",
      default_version='v1',
      description="Branch Support - Chat API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<str:ticket_id>', ticket_view, name='ticket_view'),
    path('api/chat/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/chat/', include(ticket_router.urls)),
    path('api/chat/', include(message_router.urls)),
    path('api/chat/', include(canned_message_router.urls)),
]
