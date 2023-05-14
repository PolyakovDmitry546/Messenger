from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Channel


@login_required()
def home(request):
    user = request.user
    template_name = 'home.html'
    context = {'context': {
        'user_channels': user.channel_set.all()
    }}
    return render(request, template_name, context)


@login_required()
def channel(request, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    template_name = 'channel.html'
    context = {
        'context': {
            'channel': Channel.objects.get(pk=pk),
            'user_channels': user.channel_set.all()
        }
    }
    return render(request, template_name, context)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})


"""class UserChannelsView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = 'channel/channels_panel.html'
    context_object_name = 'channel_list'

    def get_queryset(self):
        user = self.request.user
        return user.channel_set.all()
"""

"""class ChannelView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = 'channel/channel.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'user_channels': user.channel_set.all()
        })
        return context
"""

