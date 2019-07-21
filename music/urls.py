from django.conf.urls import url
from . import views
#the app_name is given so that the below html pages can be referred as the pages of this music app
app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),


    url(r'^hero/$', views.HeroesView.as_view(), name='hero-name'),

    # /music/712/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/album/add
    url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'),

    # /music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete$', views.AlbumDelete.as_view(), name='album-delete'),

    url(r'^(?P<album_id>[0-9]+)/song/add/$',views.SongCreate.as_view(),name='song-add')


]
