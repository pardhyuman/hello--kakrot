from django.contrib import admin
from .models import Album, Song,Playlist

admin.site.register(Album)
admin.site.register(Playlist)

admin.site.register(Song)
