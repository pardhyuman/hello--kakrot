from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

class Playlist(models.Model):
       user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
       atitle=models.CharField(max_length=250,default="PALACE");
       song_title = models.CharField(max_length=250,default="SONG")
       audio_file = models.CharField(max_length=550,default="FILE")
       is_favorite = models.BooleanField(default=True)
       def __str__(self):
          return self.song_title
      
	   
	   