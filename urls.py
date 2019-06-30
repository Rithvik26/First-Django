from django.conf.urls import url
from . import views
#the app_name is given so that the below html pages can be referred as the pages of this music app
app_name = 'music'

urlpatterns = (
    #/music/
    url(r'^$',views.index, name='index'),

    #/music/712/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),

    # /music/<album_id>/favorite
    #instead of typing this r'^(?P<album_id>[0-9]+)/favorite/ b $' we can use the name,i.e 'favorite' to access this page
    url(r'^(?P<album_id>[0-9]+)/favorite/ b $', views.favorite, name='favorite'),

)
