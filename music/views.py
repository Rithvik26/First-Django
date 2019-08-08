from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from .models import Hero,Album,Song
from .forms import Userform
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class HeroesView(generic.ListView):

    context_object_name = 'all_heroes'
    template_name = 'music/heroes_index.html'

    def get_queryset(self):
        return Hero.objects.all()


class HeroIndexView(generic.DetailView):
    model = Hero
    template_name = 'music/hero_detail_albums.html'



class AlbumCreate(CreateView):
    model = Album
    fields = ['hero','artist', 'album_title', 'genre', 'release', 'album_logo']
    success_url = "/music/"


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['hero','artist', 'album_title', 'genre', 'release', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'file_type', 'song_title', 'is_favorite']
    success_url = "/music/{album_id}"


class SongDelete(DeleteView):
    model = Song
    success_url = "/music/{album_id}"




class HeroCreate(CreateView):
    model = Hero
    fields = ['hero_name', 'age']
    success_url = "/music/hero"


class UserFormView(View):
    form_class = UserCreationForm
    template_name = 'music/registration_form.html'

    #get means a blank form which requires to be filled if it is a new user i.e,Register
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    # process form data after clicking on submit
    def post(self,request):
        form = self.form_class(data=request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean (normalized) data
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']
            # set the user password beçause password should be in the form of hash
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username,password=password)

            if user:

                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


class LoginViews(View):
    form_class = Userform
    template_name = 'music/login_form.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request , 'music/login_form.html', {'form':form})

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

        return render(request, self.template_name, {'form': form})


def logout_user(request):
    logout(request)
    form = Userform(request.POST)
    context = {'form':form}
    return render(request, 'music/visitor_base.html',context)
