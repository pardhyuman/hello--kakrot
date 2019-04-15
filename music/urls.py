from django.conf.urls import url
from . import views
from django.conf import settings;
from django.conf.urls.static import static 

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^displays/$', views.displays, name='displays'),
	
	url(r'^addit/$',views.addit,name='addit'),
	url(r'^$', views.index1, name='index1'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
	 url(r'^addsong/$', views.addsong, name='addsong'),
	url(r'^login_again/$', views.login_again, name='login_again'),
	url(r'^login_user123/$', views.login_user123, name='login_user123'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<album_id>[0-9]+)/$', views.detail123, name='detail123'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)