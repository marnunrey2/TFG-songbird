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
    UserSong,
)
from .spotify import spotify_api
from .deezer import deezer
from .kworb import kworb_all_time
from .appleMusic import apple_music
from .amazonMusic import amazon_music_api
from .youtube import youtube_api
from .billboard import billboard
from .lyrics import genius_lyrics, genius_lyrics_of_a_song
from .whoosh import create_whoosh_index

from rest_framework.pagination import PageNumberPagination
from rest_framework import status, filters, viewsets
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
from rest_framework.decorators import api_view

from django.contrib.auth.password_validation import validate_password, ValidationError
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.conf import settings
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.db.models.functions import Length
from django.db.models import F

import os
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser


############################# POPULATE #############################


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

    # # DELETE ALL OBJECTS
    # delete_all_objects()

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

    # # BILLBOARD
    # start_time = time.time()
    # billboard()
    # print(f"billboard took {time.time() - start_time} seconds")

    # # YOUTUBE
    # start_time = time.time()
    # youtube_api()
    # print(f"youtube_api took {time.time() - start_time} seconds")

    # # AMAZON MUSIC API NOT WORKING AT THE MOMENT
    # # amazon_music_api()

    # # GENIUS LYRICS
    # start_time = time.time()
    # genius_lyrics()
    # print(f"genius_lyrics took {time.time() - start_time} seconds")

    # # GENIUS LYRICS OF A SONG
    # genius_lyrics_of_a_song("Andrea")

    # WHOOSH
    # create_whoosh_index()

    # Query all objects from each model
    # songs = Song.objects.filter(available_at__contains=["Deezer"])
    # artists_songs = (
    #     Song.objects.select_related("main_artist")
    #     .prefetch_related("collaborators")
    #     .filter(available_at__contains=["Deezer"])
    # )
    # artists = set(song.main_artist for song in artists_songs)
    # artists.add(
    #     collaborator
    #     for song in artists_songs
    #     for collaborator in song.collaborators.all()
    # )

    genres = Genre.objects.all()
    songs = {}

    # For each genre, get the songs
    for genre in genres:
        songs[genre.name] = []
        # Get albums of the genre
        albums = Album.objects.filter(genres__name=genre.name)
        # Get songs of each album
        for album in albums:
            songs_album = album.album_songs.all()
            songs[genre.name].append(songs_album)
    # songs = Song.objects.all()
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


############################# AUTHENTICATION #############################


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

        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({"password": e.messages}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username": "This username is already in use"}, status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse({"email": "This email is already in use"}, status=400)

        # if avatar is None:
        #     default_avatar_path = os.path.join(
        #         settings.MEDIA_ROOT, "avatars\default.png"
        #     )
        #     avatar = File(open(default_avatar_path, "rb"))

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
            # profile = UserProfile.objects.filter(user=user).first()
            # if profile is not None:
            #     UserSong.objects.filter(user=profile).delete()
            #     profile.liked_songs.clear()

            user_data = model_to_dict(user)

            profile = UserProfile.objects.filter(user=user).first()

            if profile is not None:

                # profile_data = model_to_dict(profile)
                # user_data["avatar"] = request.build_absolute_uri(
                #     profile_data["avatar"].url
                # )

                # Get liked songs, albums, and artists
                user_data["liked_songs"] = list(profile.liked_songs.values())

            return JsonResponse(user_data, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


############################# USER ACTIONS #############################


@api_view(["POST"])
def like_song(request):
    user_id = request.data.get("user_id")
    song_id = request.data.get("song_id")

    user = UserProfile.objects.get(user__id=user_id)
    song = Song.objects.get(id=song_id)

    UserSong.objects.create(user=user, song=song)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def unlike_song(request):
    user_id = request.data.get("user_id")
    song_id = request.data.get("song_id")

    user = UserProfile.objects.get(user__id=user_id)
    song = Song.objects.get(id=song_id)

    user_song = UserSong.objects.get(user=user, song=song)
    user_song.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


############################# SEARCH #############################


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


### SONG ###


class SongSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            songs = Song.objects.filter(name__icontains=query)
            songs = songs.annotate(match_length=Length("name")).order_by(
                "-match_length"
            )
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


### ARTIST ###


class ArtistSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            artists = Artist.objects.filter(name__icontains=query)
            artists = artists.annotate(match_length=Length("name")).order_by(
                "-match_length"
            )
            serializer = SongSerializer(artists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


### ALBUM ###


class AlbumSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if query:
            albums = Album.objects.filter(name__icontains=query)
            albums = albums.annotate(match_length=Length("name")).order_by(
                "-match_length"
            )
            serializer = SongSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


############################# GET CERTAIN DATA #############################

### SONG ###


@api_view(["GET"])
def song_detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
        serializer = SongSerializer(song)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Song.DoesNotExist:
        return JsonResponse(
            {"error": "Song with this ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid song ID. It must be an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### ARTIST ###


@api_view(["GET"])
def artist_detail(request, artist_name):
    try:
        artist = Artist.objects.get(name=artist_name)
        serializer = ArtistSerializer(artist)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Artist.DoesNotExist:
        return JsonResponse(
            {"error": "Artist with this name does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid artist name. It must be a str."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def artist_albums(request, artist_name):
    try:
        artist = Artist.objects.get(name=artist_name)
        albums = Album.objects.filter(artist=artist)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Artist.DoesNotExist:
        return JsonResponse(
            {"error": "Artist with this name does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid artist name. It must be a str."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def artist_songs(request, artist_name):
    try:
        artist = Artist.objects.get(name=artist_name)
        songs = Song.objects.filter(main_artist=artist).order_by(
            F("release_date").desc(nulls_last=True)
        )
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Artist.DoesNotExist:
        return JsonResponse(
            {"error": "Artist with this name does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid artist name. It must be a str."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


############################# GET DATA #############################

### SONG ###


@api_view(["GET"])
def song_list(request):
    try:
        # Get songs in descending order of release date
        songs = Song.objects.all().order_by(F("release_date").desc(nulls_last=True))

        # Limit the number of songs returned
        limit = request.GET.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid limit value. It must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            songs = songs[: int(limit)]

        # Serialize the data
        serializer = SongSerializer(songs, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### ARTIST ###


@api_view(["GET"])
def artist_list(request):
    try:
        # Get artists in descending order of release date
        artists = Artist.objects.all().order_by(F("followers").desc(nulls_last=True))

        # Limit the number of artists returned
        limit = request.GET.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid limit value. It must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            artists = artists[:limit]

        # Serialize the data
        serializer = ArtistSerializer(artists, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### ALBUM ###


@api_view(["GET"])
def album_list(request):
    try:
        # Get albums in descending order of release date
        albums = Album.objects.all().order_by(F("release_date").desc(nulls_last=True))

        # Limit the number of albums returned
        limit = request.GET.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid limit value. It must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            albums = albums[:limit]

        # Serialize the data
        serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### GENRE ###


@api_view(["GET"])
def genre_list(request):
    try:
        # Get genres
        genres = Genre.objects.all()

        # Serialize the data
        serializer = GenreSerializer(genres, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# class SmallSetPagination(PageNumberPagination):
#     page_size = 25
#     page_size_query_param = "limit"
#     max_page_size = 1000

# class WebsiteViewSet(viewsets.ModelViewSet):
#     queryset = Website.objects.all()
#     serializer_class = WebsiteSerializer


# class PlaylistViewSet(viewsets.ModelViewSet):
#     queryset = Playlist.objects.all()
#     serializer_class = PlaylistSerializer
#     pagination_class = SmallSetPagination


# class PositionViewSet(viewsets.ModelViewSet):
#     queryset = Position.objects.all()
#     serializer_class = PositionSerializer
#     pagination_class = SmallSetPagination


# class PlaylistSongViewSet(viewsets.ModelViewSet):
#     queryset = PlaylistSong.objects.all()
#     serializer_class = PlaylistSongSerializer
