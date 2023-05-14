from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    #path('channels/', views.UserChannelsView.as_view(), name='user_channels'),
    path('channels/<int:pk>', views.channel, name='channel'),
    path('chat/<str:room_name>/', views.room, name='room')
]
