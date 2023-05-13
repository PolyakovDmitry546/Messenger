from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Channel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    members = models.ManyToManyField(User, through='Membership')
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='icons/')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('channel', kwargs={'pk': self.pk})


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} -> {self.channel}"


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')