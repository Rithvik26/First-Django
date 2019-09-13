from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.http import JsonResponse
from .models import Hero, Album, Song
from .forms import Userform,Songform
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .serializers import UserSerializer, AlbumSerializer
import requests
from django.utils.decorators import method_decorator

audio_file_types = ['wav', 'mp3', 'ogg']
def geo_loc(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    response = requests.get('https://api6.ipify.org?format=json', timeout=5)
    data = response.json()

    return render(request, 'music/geoloc.html', {
        'ip': data['ip'],

        'api_key': 'AIzaSyD0P17wYiOVO7KZK04VleTdt_NBYCNXuT0'

    })


@method_decorator(login_required,name='dispatch')
class IndexView(generic.ListView):
    context_object_name = 'all_albums'
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)


@method_decorator(login_required,name='dispatch')
class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


@method_decorator(login_required,name='dispatch')
class HeroesView(generic.ListView):
    context_object_name = 'all_heroes'
    template_name = 'music/heroes_index.html'

    def get_queryset(self):
        return Hero.objects.filter(user=self.request.user)


@method_decorator(login_required,name='dispatch')
class HeroIndexView(generic.DetailView):
    model = Hero
    template_name = 'music/hero_detail_albums.html'


@method_decorator(login_required,name='dispatch')
class AlbumCreate(CreateView):
    model = Album
    fields = ['hero', 'artist', 'album_title', 'genre', 'release', 'album_logo']
    success_url = "/music/"


@method_decorator(login_required,name='dispatch')
class AlbumUpdate(UpdateView):
    model = Album
    fields = ['hero', 'artist', 'album_title', 'genre', 'release', 'album_logo']


@method_decorator(login_required,name='dispatch')
class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


@login_required(login_url='/music/login')
def SongCreate(request, album_id):
    form = Songform(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)

    if form.is_valid():
        for song in album.song_set.all():
            if song.song_title==form.cleaned_data.get("song_title"):
                context={
                      'album':album,
                      'form':form,
                      'error_message':'The song already exists'
                }
                return render(request,'music/song_form.html',context)
        song = form.save(commit=False)
        song.album = album
        if song.audio_file.url.split('.')[-1] not in audio_file_types:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/song_form.html', context)
        song.save()

        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/song_form.html', context)

@method_decorator(login_required,name='dispatch')
class SongDelete(DeleteView):
    model = Song
    success_url = "/music/{album_id}"


@method_decorator(login_required,name='dispatch')
class HeroCreate(CreateView):
    model = Hero
    fields = ['hero_name', 'hero_img', 'age']
    success_url = "/music/hero"


@method_decorator(login_required,name='dispatch')
class HeroDelete(DeleteView):
    model = Hero
    success_url = reverse_lazy('music:hero-in')


class UserFormView(APIView):
    form_class = Userform
    template_name = 'music/registration_form.html'

    # get means a blank form which requires to be filled if it is a new user i.e,Register
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data after clicking on submit
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # clean (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # set the user password beçause password should be in the form of hash
            user.set_password(password)
            user.save()
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return Response(form.data, template_name=self.template_name)


class LoginViews(APIView):
    form_class = Userform
    template_name = 'music/login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'music/login_form.html', {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('music:hero-in')
            else:
                return render(request, 'music/login_form.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login_form.html', {'error_message': 'Invalid login'})

        return render(request, self.template_name)


class logout_user(APIView):

    def get(self, request):
        logout(request)

        return render(request, 'music/visitor_base.html')


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
