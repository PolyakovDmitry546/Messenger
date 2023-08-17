from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Message


class MessageAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class MessageSerializer(serializers.ModelSerializer):
    author = MessageAuthorSerializer()

    class Meta:
        model = Message
        fields = ('text', 'update_at', 'author')


class MessagePageSerializer(serializers.Serializer):
    messages = MessageSerializer(many=True)
    page = serializers.IntegerField()
    next_page = serializers.IntegerField()
