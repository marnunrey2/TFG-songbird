from django.shortcuts import render
from django.http import HttpResponse
from .populate import populate
from .models import Song, Playlist, Artist, Genre, Album
from .amazonMusic import amazon_music_api
from .spotify import spotify_api


"""
def populate_view(request):
    populate()  # Call the populate function

    # Query all objects from each model
    songs = Song.objects.all()
    artists = Artist.objects.all()
    genres = Genre.objects.all()

    # Pass the objects to the template
    context = {
        "songs": songs,
        "artists": artists,
        "genres": genres,
    }
    return render(request, "database.html", context)


"""


def populate_view(request):
    spotify_api()

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
