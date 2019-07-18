# the serializers are taking a model and saving that data in a format that we can transfer(like Json)
from rest_framework import serializers
from .models import Album


# the serializers.ModelSerializer tells that we have to serialize the data from a model


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
# we can also use fields = '__all__' which includes all the fields in that model may contain the pk
        fields = ('album_title', 'genre')


