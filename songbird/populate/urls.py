from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    populate_view,
    song_list,
    artist_list,
    album_list,
    genre_list,
    website_names,
    playlist_songs,
    song_detail,
    artist_detail,
    artist_albums,
    artist_songs,
    album_detail,
    signup,
    login,
    like_song,
    unlike_song,
    SearchView,
    SongSearchView,
    ArtistSearchView,
    AlbumSearchView,
)

# router = DefaultRouter()
# router.register(r"websites", WebsiteViewSet)
# router.register(r"playlists", PlaylistViewSet)
# router.register(r"positions", PositionViewSet)
# router.register(r"playlistsongs", PlaylistSongViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("populate/", populate_view, name="populate"),
    path("songs/", song_list, name="song-list"),
    path("artists/", artist_list, name="artist-list"),
    path("albums/", album_list, name="album-list"),
    path("genres/", genre_list, name="genre-list"),
    path("website_names/<str:playlist_name>/", website_names, name="website_names"),
    path(
        "playlist_songs/<str:playlist_name>/<str:website_name>/",
        playlist_songs,
        name="playlist_songs",
    ),
    # SEARCH
    path("search/", SearchView.as_view(), name="general-search"),
    path("songs-search/", SongSearchView.as_view(), name="song-search"),
    path("artists-search/", ArtistSearchView.as_view(), name="artist-search"),
    path("albums-search/", AlbumSearchView.as_view(), name="album-search"),
    # USER
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    # USER ACTIONS
    path("user/like_song/", like_song, name="like_song"),
    path("user/unlike_song/", unlike_song, name="unlike_song"),
    # DETAILS
    path("songs/<int:song_id>/", song_detail, name="song-detail"),
    path("artists/<str:artist_name>/", artist_detail, name="song-detail"),
    path("artists/<str:artist_name>/albums", artist_albums, name="artist-albums"),
    path("artists/<str:artist_name>/songs", artist_songs, name="artist-songs"),
    path("albums/<int:album_id>/", album_detail, name="album-detail"),
]
