from django.contrib import admin
from .models import Album,Song,Hero

# whenever you register we can add and delete your model fields on admin panel
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Hero)
