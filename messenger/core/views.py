from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ChannelCreationForm
from .models import Channel
from .serializers import MessagePageSerializer
from .services import ChannelMessagesPageService


@login_required()
def home(request):
    user = request.user
    template_name = 'home.html'
    context = {'context': {
        'user_channels': user.channel_set.all(),
    }}
    return render(request, template_name, context)


@login_required()
def channel_create(request: HttpRequest):
    template_name = 'channel_create.html'

    if request.method == 'GET':
        context = {
            'form': ChannelCreationForm(),
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = ChannelCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_channel: Channel = form.save(commit=False)
            user = request.user
            new_channel.author = user
            new_channel.save()
            new_channel.members.add(user)
            return redirect('home')

        context = {
            'form': form,
        }
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
            'messages_url': reverse('messages', kwargs={'pk': pk}),
        },
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
    obj = dict(messages=channel_service.get_messages(),
               page=channel_service.get_page(), next_page=channel_service.get_next_page())
    serializer = MessagePageSerializer(obj)
    return JsonResponse(serializer.data, safe=False)


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
