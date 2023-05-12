from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=gettext_lazy('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta():
        model = User
        fields = ('username', 'email')
