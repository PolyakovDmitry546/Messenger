from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('channel/create', views.ChannelCreateView.as_view(), name='channel_create'),
    path('channels/<int:pk>', views.ChannelView.as_view(), name='channel'),
    path('api/v1/channels/<int:pk>/messages', views.ChannelMessagesAPIView.as_view(), name='messages'),
    path('api/v1/search', views.SearchResultAPIView.as_view(), name='search'),
]
