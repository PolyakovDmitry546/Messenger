from django import forms

from .models import Channel


class ChannelCreationForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['icon', 'name', 'description']
