from django.shortcuts import render
from .models import (
    Song,
    Playlist,
    Artist,
    Genre,
    Album,
    PlaylistSong,
    Website,
    Position,
)
from .spotify import spotify_api
from .deezer import deezer
from .kworb import kworb_all_time
from .appleMusic import apple_music
from .amazonMusic import amazon_music_api
from .youtube import youtube_api
from .billboard import billboard
from .lyrics import genius_lyrics

from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .serializers import (
    GenreSerializer,
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    WebsiteSerializer,
    PlaylistSerializer,
    PositionSerializer,
    PlaylistSongSerializer,
)


def delete_all_objects():
    Song.objects.all().delete()
    Playlist.objects.all().delete()
    Artist.objects.all().delete()
    Genre.objects.all().delete()
    Album.objects.all().delete()
    PlaylistSong.objects.all().delete()
    Website.objects.all().delete()
    Position.objects.all().delete()


def populate_view(request):

    # spotify_api()
    # apple_music()
    # kworb_all_time()
    # deezer()
    # youtube_api()
    # billboard()

    # AMAZON MUSIC API NOT WORKING AT THE MOMENT
    # amazon_music_api()

    # genius_lyrics()

    # Query all objects from each model
    songs = Song.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all()
    genres = Genre.objects.all()
    playlists = Playlist.objects.all()
    websites = Website.objects.all()
    playlists_songs = Playlist.objects.prefetch_related("playlist_songs").all()

    # Pass the objects to the template
    context = {
        "songs": songs,
        "artists": artists,
        "albums": albums,
        "playlists": playlists,
        "genres": genres,
        "websites": websites,
        "playlists_songs": playlists_songs,
    }
    return render(request, "database.html", context)


class SmallSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "limit"
    max_page_size = 1000


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = SmallSetPagination


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = SmallSetPagination


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = SmallSetPagination


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = SmallSetPagination


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = SmallSetPagination


class PlaylistSongViewSet(viewsets.ModelViewSet):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer
