from django.db import models
from django.urls import reverse

from django.contrib.auth.models import Permission, User

# whenever u create or alter a model then go to terminal and write 'python manage.py makemigrations' and
# 'python manage.py migrate'-this creates the table for ur current structure


class Hero(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    hero_name = models.CharField(max_length=15)
    hero_img = models.FileField(default=1)
    age = models.IntegerField()

    # Meta replaces name on admin page
    class Meta:
        verbose_name_plural = "Hero"

    def __str__(self):
        return self.hero_name


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    hero = models.ForeignKey(Hero, default=1, verbose_name="Hero",on_delete=models.CASCADE)
    artist = models.CharField(max_length=200)
    album_title = models.CharField(max_length=400)
    genre = models.CharField(max_length=10)
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





