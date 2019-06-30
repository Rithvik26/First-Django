#from django.http import Http404
#from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Album,Song


def index(request):
    all_albums = Album.objects.all()
    return render(request, 'music/index.html', {'all_albums':all_albums})


def detail(request, album_id):
    #try:
        #album =Album.objects.get(id=album_id)
    #except Album.DoesNotExist:
        #raise Http404("The Album does not exist")
    album = get_object_or_404(Album,id=album_id)
    return render(request,'music/detail.html',{'album' : album})

def favorite(request, album_id):
    album = get_object_or_404(Album,id=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html',{
            'album' : album,
            'error_message':"You did not select any valid song"
        })

    else:

        selected_song.is_favorite = not selected_song.is_favorite
        selected_song.save()
        return render(request,'music/detail.html',{'album' : album})




