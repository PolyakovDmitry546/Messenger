from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Channel, Message


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


class SearchResultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class SearchResultChannelSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Channel
        fields = ('name', 'url')


class SearchResultSerializer(serializers.Serializer):
    users = SearchResultUserSerializer(many=True)
    channels = SearchResultChannelSerializer(many=True)
