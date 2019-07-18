from django.db import models
from django.urls import reverse


# whenever u create or alter a model then go to terminal and write 'python manage.py makemigrations' and
# 'python manage.py migrate'-this creates the table for ur current structure
class Hero(models.Model):
    hero_name = models.CharField(max_length=15)
    movie = models.CharField(max_length=15)
    song_name = models.CharField(max_length=10)

    def __str__(self):
        return self.hero_name

class Album(models.Model):
    artist = models.CharField(max_length=200)
    album_title = models.CharField(max_length=400)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    release = models.IntegerField()
    album_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})


    def __str__(self):
        return self.album_title + ' - '+self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=200)
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.song_title



