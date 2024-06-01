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
    UserProfile,
)
from .spotify import spotify_api
from .deezer import deezer
from .kworb import kworb_all_time
from .appleMusic import apple_music
from .amazonMusic import amazon_music_api
from .youtube import youtube_api
from .billboard import billboard
from .lyrics import genius_lyrics
from .whoosh import create_whoosh_index

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.conf import settings
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict

import os
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser


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

    # # SPOTIFY
    # start_time = time.time()
    # spotify_api()
    # print(f"spotify_api took {time.time() - start_time} seconds")

    # # APPLE MUSIC
    # start_time = time.time()
    # apple_music()
    # print(f"apple_music took {time.time() - start_time} seconds")

    # # KWORB
    # start_time = time.time()
    # kworb_all_time()
    # print(f"kworb_all_time took {time.time() - start_time} seconds")

    # # DEEZER
    # start_time = time.time()
    # deezer()
    # print(f"deezer took {time.time() - start_time} seconds")

    # # YOUTUBE
    # start_time = time.time()
    # youtube_api()
    # print(f"youtube_api took {time.time() - start_time} seconds")

    # # BILLBOARD
    # start_time = time.time()
    # billboard()
    # print(f"billboard took {time.time() - start_time} seconds")

    # # AMAZON MUSIC API NOT WORKING AT THE MOMENT
    # # amazon_music_api()

    # # GENIUS LYRICS
    # start_time = time.time()
    # genius_lyrics()
    # print(f"genius_lyrics took {time.time() - start_time} seconds")

    # WHOOSH
    create_whoosh_index()

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


@csrf_exempt
def signup(request):
    if request.method == "POST":
        # User.objects.all().delete()
        # UserProfile.objects.all().delete()
        # print(User.objects.all())
        # print(UserProfile.objects.all())

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        avatar = request.FILES.get("avatar")

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username": "This username is already in use"}, status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse({"email": "This email is already in use"}, status=400)

        if avatar is None:
            default_avatar_path = os.path.join(
                settings.MEDIA_ROOT, "avatars\default.png"
            )
            avatar = File(open(default_avatar_path, "rb"))

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user_profile = UserProfile.objects.create(user=user, avatar=avatar)
        user_profile.save()

        return JsonResponse({"message": "User created successfully"}, status=201)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_data = model_to_dict(user)

            profile = UserProfile.objects.filter(user=user).first()

            if profile is not None:

                profile_data = model_to_dict(profile)
                user_data["avatar"] = request.build_absolute_uri(
                    profile_data["avatar"].url
                )

                # Get liked songs, albums, and artists
                user_data["liked_songs"] = list(profile.liked_songs.values())
                user_data["liked_albums"] = list(profile.liked_albums.values())
                user_data["liked_artists"] = list(profile.liked_artists.values())

            return JsonResponse(user_data, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def search_songs(request):
    # Get the search term from the request
    search_term = request.GET.get("search", "")

    # Open the index
    index = open_dir("indexwhoosh/song")

    # Search the index
    with index.searcher() as searcher:
        query = QueryParser("name", index.schema).parse(search_term)
        results = searcher.search(query)
        songs = [hit.fields() for hit in results]

    # Return the search results as JSON
    return JsonResponse(songs, safe=False)


class SongSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            songs = Song.objects.filter(name__icontains=query)
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


class ArtistSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            artists = Artist.objects.filter(name__icontains=query)
            serializer = SongSerializer(artists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


class AlbumSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            albums = Album.objects.filter(name__icontains=query)
            serializer = SongSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


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
