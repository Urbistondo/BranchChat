from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ticket, Message


User = get_user_model()


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'id',
            'user_id',
            'agent_id',
            'has_disconnected',
            'category',
            'priority',
            'status',
            'subject',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'subject')

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.agent = validated_data.get('agent', instance.agent)
        instance.has_disconnected = validated_data.get('has_disconnected', instance.has_disconnected)
        instance.category = validated_data.get('category', instance.category)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.subject = validated_data.get('subject', instance.subject)

        instance.save()

        return instance


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'author',
            'body',
            'ticket',
            'sent_at',
        )
        read_only_fields = ('id', 'author', 'body', 'ticket', 'sent_at')
