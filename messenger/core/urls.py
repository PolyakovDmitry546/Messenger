from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('channels/', views.UserChannelsView.as_view(), name='user_channels'),
    path('channel/create', views.channel_create, name='channel_create'),
    path('channels/<int:pk>', views.channel, name='channel'),
    path('channels/<int:pk>/messages', views.get_messages, name='messages'),
    path('api/v1/search', views.SearchResultAPIView.as_view(), name='search'),
]
