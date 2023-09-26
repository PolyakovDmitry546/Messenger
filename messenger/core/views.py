from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from rest_framework import permissions
from rest_framework.views import APIView, Response

from .forms import ChannelCreationForm
from .models import Channel, Dialog, DialogMembership
from .serializers import ChannelMessagePageSerializer, DialogMessagePageSerializer, SearchResultSerializer
from .services import ChannelMessagesPageService, DialogMessagesPageService


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        user = self.request.user
        context = {'context': {
            'user_channels': user.channel_set.all(),
        }}
        return context


class ChannelCreateView(LoginRequiredMixin, FormView):
    template_name = 'channel_create.html'
    form_class = ChannelCreationForm

    def get_success_url(self) -> str:
        return reverse('home')

    def form_valid(self, form) -> HttpResponse:
        new_channel: Channel = form.save(commit=False)
        user = self.request.user
        new_channel.author = user
        new_channel.save()
        new_channel.members.add(user)
        return super().form_valid(form)


class ChannelView(LoginRequiredMixin, TemplateView):
    template_name = 'channel.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user
        context = {
            'context': {
                'channel': Channel.objects.get(pk=pk),
                'user_channels': user.channel_set.all(),
                'messages_url': reverse('messages', kwargs={'pk': pk}),
            },
        }
        return context


class ChannelJoinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'channel_join.html'
        pk = kwargs.get('pk')
        user = request.user
        channel = Channel.objects.get(pk=pk)

        if channel.members.contains(user):
            return redirect('channel', pk=pk)

        context = {
            'context': {
                'channel': channel,
                'user_channels': user.channel_set.all(),
            },
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        channel = Channel.objects.get(pk=pk)
        channel.members.add(user)
        return redirect('channel', pk=pk)


class DialogView(LoginRequiredMixin, TemplateView):
    template_name = 'dialog.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user
        dialog = Dialog.objects.get(pk=pk)
        context = {
            'context': {
                'dialog': dialog,
                'target_user': DialogMembership.objects.filter(chat=dialog).exclude(user=user).first().user,
                'user_channels': user.channel_set.all(),
                'messages_url': reverse('dialog_messages', kwargs={'pk': pk}),
            },
        }
        return context


class DialogJoinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'dialog_join.html'
        target_user_pk = kwargs.get('pk')
        target_user = User.objects.get(pk=target_user_pk)
        user = request.user

        if (dialog := Dialog.get_dialog(user1=user, user2=target_user)) is not None:
            return redirect('dialog', pk=dialog.pk)

        context = {
            'context': {
                'dialog': None,
                'user_channels': user.channel_set.all(),
            },
        }
        return render(request, template_name, context)


class ChannelMessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        page = request.GET.get('page', default=None)
        page = int(page) if page is not None else None
        per_page = request.GET.get('per_page', default=None)
        per_page = int(per_page) if per_page is not None else None
        channel_pk = kwargs.get('pk')

        channel_service = ChannelMessagesPageService(request.user, channel_pk, page, per_page)
        obj = dict(messages=channel_service.get_messages(),
                   page=channel_service.get_page(), next_page=channel_service.get_next_page())
        serializer = ChannelMessagePageSerializer(obj)
        return Response(serializer.data)


class DialogMessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        page = request.GET.get('page', default=None)
        page = int(page) if page is not None else None
        per_page = request.GET.get('per_page', default=None)
        per_page = int(per_page) if per_page is not None else None
        dialog_pk = kwargs.get('pk')

        dialog_service = DialogMessagesPageService(request.user, dialog_pk, page, per_page)
        obj = dict(messages=dialog_service.get_messages(),
                   page=dialog_service.get_page(), next_page=dialog_service.get_next_page())
        serializer = DialogMessagePageSerializer(obj)
        return Response(serializer.data)


class SearchResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.GET.get('q', default=None)
        if q is None or q == '':
            return Response({'users': [], 'channels': []})
        users = User.objects.filter(username__icontains=q)
        channels = Channel.objects.filter(name__icontains=q)
        serializer = SearchResultSerializer(dict(users=users, channels=channels))
        return Response(serializer.data)
