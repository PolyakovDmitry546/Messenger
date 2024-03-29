from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import Channel
from .services import ChannelMessagesPageService
from .serializers import MessagePageSerializer
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
    page = request.GET.get('page', default=None)
    page = int(page) if page is not None else None
    per_page = request.GET.get('per_page', default=None)
    per_page = int(per_page) if per_page is not None else None
    channel_pk = kwargs.get('pk')

    channel_service = ChannelMessagesPageService(request.user, channel_pk, page, per_page)
    obj = dict(messages=channel_service.get_messages(), page=channel_service.get_page(), next_page=channel_service.get_next_page())
    serializer = MessagePageSerializer(obj)
    return JsonResponse(serializer.data, safe=False)


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

