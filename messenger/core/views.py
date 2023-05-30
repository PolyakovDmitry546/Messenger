from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import Channel, Message
from . import DTO


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
            'user_channels': user.channel_set.all(),
            'messages_url': reverse('messages', kwargs={'pk': pk})
        }
    }
    return render(request, template_name, context)


@login_required()
def get_messages(request, **kwargs):
    pk = kwargs.get('pk')
    messages = Channel.objects.get(pk=pk).get_messages()
    data = []
    mes: Message
    for mes in messages:
        data.append(
            DTO.Message(
                mes.author.pk,
                mes.author.get_username(),
                mes.text,
                mes.update_at
            )
        )
    data = DTO.MessageList(data)
    return JsonResponse(data.to_json(), safe=False)


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

