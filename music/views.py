from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song,Playlist
import pickle;
import os;

#from django.contrib.auth.models import User

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user;
        username = request.user.username;
        if (username=='SongPalace'):
              album = get_object_or_404(Album, pk=album_id)
              return render(request, 'music/detail123.html', {'album': album, 'user': user})
        else: 
              user = request.user
              album = get_object_or_404(Album, pk=album_id)
              return render(request, 'music/detail.html', {'album': album, 'user': user})
 
def detail123(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail123.html', {'album': album, 'user': user})

		
def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})
			
def index1(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index1.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index1.html', {'albums': albums})			


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        cwd=os.getcwd();
        print(cwd);
        filename='fora'
        outfile=open(filename,'wb');
        pickle.dump(username,outfile);
        outfile.close();
        filename2='forb'
        outfile2=open(filename2,'wb');
        pickle.dump(password,outfile2);
        outfile2.close();
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')
	
	
def login_again(request):
    
        infile=open('fora','rb');
        user1=pickle.load(infile);
        infile.close();
        print(user1);
        print("\n");	
        infile2=open('forb','rb');
        pass1=pickle.load(infile2);
        username = user1
        password = pass1;
        cwd=os.getcwd();
        print(cwd);
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    	
def addit(request):###when you click on submit in add to favourite of our collection
        sear=request.POST.get('search');###url of song when you click on submit in add to favourite of our collection
        tit=request.POST.get('title');#title of song
        
		#print(y);to print URL of song and name of song
		
        print("******************************************************\n")
        print(sear);
        print(tit);
		
		##to login back to user  and logout from universal user automatically
		##picking up detail with  pickle
        infile=open('fora','rb');
        user1=pickle.load(infile);
        infile.close();
        print(user1);
        print("\n");	
        infile2=open('forb','rb');
        pass1=pickle.load(infile2);
		
		##to pickle out link and name of song i.e sear and tit
        filename1='arc1'
        outfile=open(filename1,'wb');
        pickle.dump(sear,outfile);
        outfile.close();
        filename2='arc2'
        outfile2=open(filename2,'wb');
        pickle.dump(tit,outfile2);
        outfile2.close();
		
        username = user1
        password = pass1;
        cwd=os.getcwd();
        print(cwd);
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                infile=open('arc1','rb');
                addr=pickle.load(infile);
                infile.close();
                print("\n");	
                infile2=open('arc2','rb');
                stitle=pickle.load(infile2);
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
                print(stitle)				
                playlists=Playlist.objects.filter(user=request.user);
                for playlist in playlists:
                    if(playlist.atitle=="PALACE"):
                       print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                       atitle1=playlist.atitle;
                       print(atitle1);                
                       return render(request, 'music/create_song2.html', {'stitle': stitle,'addr':addr,'atitle1':atitle1})
                
                
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
				
				
        
        return render(request, 'music/abc.html');
					
					
def addsong(request):
      #playlists=request.
      #addr1=request.POST['addr'];
      addr1 = request.POST.get('addr')
      #stitle1=request.POST['stitle'];
      stitle1 = request.POST.get('stitle')
      atitle2=request.POST.get('atitle1');
      user3=request.user
      cwd=request.build_absolute_uri('/');
      print(cwd);
      print("++++++++++++++++++++++++++++++++++++++++++++++++++");
      print(atitle2)
      print(stitle1)
      print(addr1)
      print("++++++++++++++++++++++++++++++++++++++++++++++++++")
	  
      p=Playlist();
      p.user=user3;
      p.atitle=atitle2;
      p.song_title=stitle1;
      p.audio_file=addr1;
      p.is_favorite=True;
      p.save();
      playlists=Playlist.objects.filter(user=request.user);
      return render(request, 'music/display.html', {'playlists': playlists,'cwd':cwd})

   					
					
def login_user123(request):
        username = 'SongPalace'
        password = 'songpalace123'
        user = authenticate(username='SongPalace', password='songpalace123')
        login(request, user);
        albums = Album.objects.filter(user=request.user);
        #render(request, 'music/songs.html', {'albums': albums})
        #input("Press enter to continue");
        return render(request, 'music/index1.html', {'albums': albums})
         
'''        if user is not None:
            if user.is_active:
			    #print("ifactive");
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index1.html', {'albums': albums})
            else:
			    #print("else active");
				
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            username = 'SongPalace'
            password = 'songpalace123'
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    albums = Album.objects.filter(user=request.user)
                    return render(request, 'music/index1.html', {'albums': albums})
                else:
                    return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
            else:		
                return render(request, 'music/login.html', {'error_message': 'Invalid login'})
'''

def displays(request):
    
    cwd=request.build_absolute_uri('/');
    print("#########################3###")
    print(cwd)
    playlists=Playlist.objects.filter(user=request.user);
    return render(request, 'music/display.html', {'playlists': playlists,'cwd':cwd})

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        filename='fora'
        outfile=open(filename,'wb');
        pickle.dump(username,outfile);
        outfile.close();
        filename2='forb'
        outfile2=open(filename2,'wb');
        pickle.dump(password,outfile2);
        outfile2.close();
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
				
                p=Playlist();
                p.user=request.user;
                p.atitle="PALACE";
                p.song_title="RANDOMSONG";
                p.audio_file="NOURL";
                p.is_favorite=True;
                p.save();
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })