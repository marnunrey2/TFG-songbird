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
from .management.commands.lyrics import genius_lyrics, genius_lyrics_of_a_song
from .management.commands.whoosh import index_data

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
    UserSongSerializer,
    UserProfileSerializer,
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

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from django.conf import settings
from .recommendations import recommend_songs


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

    print("Populating database...")

    # SPOTIFY
    start_time = time.time()
    print("\nSpotify API: starting...")
    spotify_api()
    print(f"Spotify API: took {time.time() - start_time} seconds")

    # APPLE MUSIC
    start_time = time.time()
    print("\nApple Music: starting...")
    apple_music()
    print(f"Apple Music: took {time.time() - start_time} seconds")

    # KWORB
    start_time = time.time()
    print("\nKworb: starting...")
    kworb_all_time()
    print(f"Kworb: took {time.time() - start_time} seconds")

    # DEEZER
    start_time = time.time()
    print("\nDeezer: starting...")
    deezer()
    print(f"Deezer: took {time.time() - start_time} seconds")

    # BILLBOARD
    start_time = time.time()
    print("\nBillboard: starting...")
    billboard()
    print(f"Billboard: took {time.time() - start_time} seconds")

    # YOUTUBE
    start_time = time.time()
    print("\nYoutube: starting...")
    youtube_api()
    print(f"Youtube: took {time.time() - start_time} seconds")

    # # AMAZON MUSIC API NOT WORKING AT THE MOMENT
    # amazon_music_api()

    # GENIUS LYRICS
    start_time = time.time()
    print("\nGenius: starting...")
    genius_lyrics()
    print(f"Genius: took {time.time() - start_time} seconds")

    # # GENIUS LYRICS OF A SONG
    # genius_lyrics_of_a_song("ME! (feat. Brendon Urie of Panic! At The Disco)")

    # WHOOSH
    index_data()

    # User.objects.all().delete()
    # UserProfile.objects.all().delete()
    # print(User.objects.all())
    # print(UserProfile.objects.all())

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


############################# AUTHENTICATION #############################


@csrf_exempt
def signup(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

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

        user_profile = UserProfile.objects.create(user=user)
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
            if user.is_superuser:
                return JsonResponse(user_data, status=200)
            else:
                profile = UserProfile.objects.filter(user=user).first()

                if profile is not None:

                    user_data["liked_songs"] = []

                    # profile_data = model_to_dict(profile)
                    # user_data["avatar"] = request.build_absolute_uri(
                    #     profile_data["avatar"].url
                    # )

                    # Serialize the profile data
                    serializer = UserProfileSerializer(profile)

                    # Get liked songs, albums, and artists
                    songs = serializer.data["liked_songs"]
                    for song in songs:
                        user_data["liked_songs"].append(song["song"])

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


############################# RECOMMENDATIONS #############################


@api_view(["GET"])
def recommend_songs_view(request, user_id):
    try:
        user = UserProfile.objects.get(user__id=int(user_id))
        recommendations = recommend_songs(user)
        return JsonResponse(recommendations, safe=False, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return JsonResponse(
            {"error": "User profile does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError as e:
        return JsonResponse(
            {"error": "Invalid user ID. It must be an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": e},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


############################# SEARCH #############################

### GENERAL SEARCH ###


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        results = []

        if query:
            ix = open_dir(settings.WHOOSH_INDEX)
            with ix.searcher() as searcher:
                parser = MultifieldParser(["content"], schema=ix.schema)
                q = parser.parse(query)
                search_results = searcher.search(q, limit=None)

                for result in search_results:
                    if result["type"] == "song":
                        instance = Song.objects.get(pk=int(result["id"].split("_")[1]))
                        results.append(
                            {"type": "song", "data": SongSerializer(instance).data}
                        )
                    elif result["type"] == "artist":
                        instance = Artist.objects.get(pk=result["id"].split("_")[1])
                        results.append(
                            {"type": "artist", "data": ArtistSerializer(instance).data}
                        )
                    elif result["type"] == "album":
                        instance = Album.objects.get(pk=int(result["id"].split("_")[1]))
                        results.append(
                            {"type": "album", "data": AlbumSerializer(instance).data}
                        )
                    elif result["type"] == "lyrics":
                        instance = Song.objects.get(pk=int(result["id"].split("_")[1]))
                        results.append(
                            {"type": "lyrics", "data": SongSerializer(instance).data}
                        )

                # Custom sort order
                sort_order = {"song": 1, "artist": 2, "album": 3, "lyrics": 4}
                results.sort(key=lambda x: sort_order.get(x["type"], 5))

            return Response(results, status=status.HTTP_200_OK)
        return Response(
            {"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST
        )


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


### ALBUM ###


@api_view(["GET"])
def album_detail(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        songs = Song.objects.filter(album=album)
        song_serializer = SongSerializer(songs, many=True)
        album_serializer = AlbumSerializer(album)
        album_data = album_serializer.data
        album_data["songs"] = song_serializer.data
        return JsonResponse(album_data, safe=False, status=status.HTTP_200_OK)
    except Album.DoesNotExist:
        return JsonResponse(
            {"error": "Album with this ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid album ID. It must be an integer."},
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

        # Filter by genre
        genre = request.GET.get("genre")
        if genre is not None:
            artists = Artist.objects.filter(genres__name=genre)
            songs = songs.filter(main_artist__in=artists)

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

        # Filter by genre
        genre = request.GET.get("genre")
        if genre is not None:
            artists = artists.filter(genres__name=genre)

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

        # Filter by genre
        genre = request.GET.get("genre")
        if genre is not None:
            artists = Artist.objects.filter(genres__name=genre)
            albums = albums.filter(artist__in=artists)

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
        genres = [genre.name for genre in Genre.objects.all()]

        return JsonResponse(genres, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### PLAYLIST ###


@api_view(["GET"])
def playlist_songs(request, playlist_name, website_name):
    try:
        playlist = Playlist.objects.get(name=playlist_name, website__name=website_name)
        playlist_songs = PlaylistSong.objects.filter(playlist=playlist)
        serializer = PlaylistSongSerializer(playlist_songs, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Playlist.DoesNotExist:
        return JsonResponse(
            {"error": "Playlist not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JsonResponse(
            {"error": "Invalid playlist name or website name."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


### WEBSITE ###


@api_view(["GET"])
def website_names(request, playlist_name):
    try:
        playlists = Playlist.objects.filter(name=playlist_name)
        website_names = [
            playlist.website.name
            for playlist in playlists
            if playlist.website is not None
        ]
        return JsonResponse(website_names, safe=False, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


############################# ADMIN #############################


@api_view(["GET"])
def admin_dashboard(request):
    try:
        num_users = User.objects.count()
        num_songs = Song.objects.count()
        num_artists = Artist.objects.count()
        num_albums = Album.objects.count()
        num_playlists = Playlist.objects.count()

        return JsonResponse(
            {
                "num_users": num_users,
                "num_songs": num_songs,
                "num_artists": num_artists,
                "num_albums": num_albums,
                "num_playlists": num_playlists,
            },
            safe=False,
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class PopulateDatabaseView(APIView):
    def post(self, request, format=None):
        try:

            print("Populating database...")
            start_time = time.time()

            # SPOTIFY
            spotify_api()
            print(f"Spotify API done. Time: {time.time()}")

            # APPLE MUSIC
            apple_music()
            print(f"Apple Music done. Time: {time.time()}")

            # KWORB
            kworb_all_time()
            print(f"Kworb done. Time: {time.time()}")

            # DEEZER
            deezer()
            print(f"Deezer done. Time: {time.time()}")

            # BILLBOARD
            billboard()
            print(f"Billboard done. Time: {time.time()}")

            # YOUTUBE
            # youtube_api()
            # print(f"Youtube done. Time: {time.time()}")

            # AMAZON MUSIC API NOT WORKING AT THE MOMENT
            # amazon_music_api()
            # print(f"Amazon Music done. Time: {time.time()}")

            # GENIUS LYRICS
            # genius_lyrics()
            # print(f"Genius Lyrics done. Time: {time.time()}")

            # WHOOSH
            index_data()
            print(f"Whoosh done. Time: {time.time()}")

            elapsed_time = time.time() - start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            formatted_time = "{:0>2}:{:0>2}:{:02}".format(
                int(hours), int(minutes), int(seconds)
            )
            message = (
                f"Database populated successfully! Took {formatted_time} to complete"
            )

            return Response({"message": message}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
