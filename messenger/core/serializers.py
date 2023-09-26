from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Channel, ChannelMessage, DialogMessage


class MessageAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ChannelMessageSerializer(serializers.ModelSerializer):
    author = MessageAuthorSerializer()

    class Meta:
        model = ChannelMessage
        fields = ('text', 'update_at', 'author')


class ChannelMessagePageSerializer(serializers.Serializer):
    messages = ChannelMessageSerializer(many=True)
    page = serializers.IntegerField()
    next_page = serializers.IntegerField()


class DialogMessageSerializer(serializers.ModelSerializer):
    author = MessageAuthorSerializer()

    class Meta:
        model = DialogMessage
        fields = ('text', 'update_at', 'author')


class DialogMessagePageSerializer(serializers.Serializer):
    messages = ChannelMessageSerializer(many=True)
    page = serializers.IntegerField()
    next_page = serializers.IntegerField()


class SearchResultUserSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'url')


class SearchResultChannelSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_join_absolute_url', read_only=True)

    class Meta:
        model = Channel
        fields = ('name', 'url')


class SearchResultSerializer(serializers.Serializer):
    users = SearchResultUserSerializer(many=True)
    channels = SearchResultChannelSerializer(many=True)
