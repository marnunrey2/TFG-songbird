from django.shortcuts import render
from .models import Song, Playlist, Artist, Genre, Album, PlaylistSong, Website
from .spotify import spotify_api
from .deezer import deezer
from .amazonMusic import amazon_music_api


def populate_view(request):

    spotify_api()

    # Query all objects from each model
    songs = Song.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all()
    playlists = Playlist.objects.all()

    # Pass the objects to the template
    context = {
        "songs": songs,
        "artists": artists,
        "albums": albums,
        "playlists": playlists,
    }
    return render(request, "database.html", context)
