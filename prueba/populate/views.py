from django.shortcuts import render
from django.http import HttpResponse
from .populate import populate
from .models import Song, Playlist, Artist, Genre, Album
from .amazonMusic import amazon_music_api
from .spotify import spotify_api
from .shazam import shazam_api
from .deezer import deezer

# from .soundcloud import soundcloud_scrapping
from .kworb import kworb_scrapping

"""
def populate_view(request):
    songs, artists, albums = deezer()  # Call the populate function

    # Pass the objects to the template
    context = {
        "songs": songs,
        "artists": artists,
        "albums": albums,
    }
    return render(request, "database.html", context)


"""


def populate_view(request):
    Song.objects.all().delete()
    Artist.objects.all().delete()
    Album.objects.all().delete()
    Genre.objects.all().delete()
    Playlist.objects.all().delete()

    spotify_api()  # Call the populate function

    # Query all objects from each model
    songs = Song.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all()

    # Pass the objects to the template
    context = {
        "songs": songs,
        "artists": artists,
        "albums": albums,
    }
    return render(request, "database.html", context)


"""

def populate_view(request):
    songs = deezer()

    return render(request, "example.html", {"songs": songs})

"""
