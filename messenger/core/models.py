from typing import Self

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Chat(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)


class Channel(Chat):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_channels')
    members = models.ManyToManyField(User, through='ChannelMembership')
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='icons/')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('channel', kwargs={'pk': self.pk})

    def get_join_absolute_url(self):
        return reverse('channel_join', kwargs={'pk': self.pk})


class Dialog(Chat):
    members = models.ManyToManyField(User, through='DialogMembership')

    def __str__(self) -> str:
        return f"Dialog: {self.pk}"

    @classmethod
    def get_dialog(cls, user1: User, user2: User) -> Self | None:
        return cls.objects.filter(user=user1).filter(user=user2).first()


class ChatMembership(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read_message_pk = models.BigIntegerField(default=0)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} -> {self.chat}"

    def read_message_count(self):
        return self.chat.messages.filter(pk__lte=self.last_read_message_pk).count()

    def unread_message_count(self):
        return self.chat.messages.filter(pk__gt=self.last_read_message_pk).count()

    def get_number_page_with_last_read_message(self, per_page):
        return self.read_message_count() // per_page


class DialogMembership(ChatMembership):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs')
    chat = models.ForeignKey(Dialog, on_delete=models.CASCADE)


class ChannelMembership(ChatMembership):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    chat = models.ForeignKey(Channel, on_delete=models.CASCADE)


class Message(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True, null=True)


class ChannelMessage(Message):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_messages')
    text = models.CharField(max_length=1000)
    owner = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')


class DialogMessage(Message):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialog_messages')
    text = models.CharField(max_length=500)
    owner = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')


class Comment(models.Model):
    class Meta:
        abstract = True

    text = models.TextField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class ChannelComment(Comment):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_comments')
    message = models.ForeignKey(ChannelMessage, on_delete=models.CASCADE, related_name='comments')
