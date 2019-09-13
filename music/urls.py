from django.conf.urls import url,include,re_path
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views
#the app_name is given so that the below html pages can be referred as the pages of this music app
app_name = 'music'


urlpatterns = [

    url(r'location/$', views.geo_loc, name='geo-in'),

    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^hero/(?P<pk>[0-9]+)/$', views.HeroIndexView.as_view(), name='index-h'),


    # /music/712/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'hero/$', views.HeroesView.as_view(), name='hero-in'),

    #/music/album/add
    url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'),

    # /music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),


    url(r'^(?P<album_id>[0-9]+)/song/add/$',views.SongCreate, name='song-create'),

    url(r'song/(?P<pk>[0-9]+)/delete/$', views.SongDelete.as_view(), name='song-delete'),

    url(r'^hero/add/$', views.HeroCreate.as_view(), name='hero-add'),

    url(r'hero/(?P<pk>[0-9]+)/delete/$', views.HeroDelete.as_view(), name='hero-delete'),

    url(r'login/$',views.LoginViews.as_view(),name='login'),

    url(r'logout_user/$', views.logout_user.as_view(), name='logout'),

    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

]
