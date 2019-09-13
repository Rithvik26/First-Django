#imports the generic user class that we can use
from django.contrib.auth.models import User
from .models import Song
from django import forms

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class Songform(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']
