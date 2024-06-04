from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    populate_view,
    GenreViewSet,
    ArtistViewSet,
    AlbumViewSet,
    SongViewSet,
    WebsiteViewSet,
    PlaylistViewSet,
    PositionViewSet,
    PlaylistSongViewSet,
    signup,
    login,
    like_song,
    unlike_song,
    search_songs,
    SongSearchView,
    ArtistSearchView,
    AlbumSearchView,
)

router = DefaultRouter()
router.register(r"genres", GenreViewSet)
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"songs", SongViewSet)
router.register(r"websites", WebsiteViewSet)
router.register(r"playlists", PlaylistViewSet)
router.register(r"positions", PositionViewSet)
router.register(r"playlistsongs", PlaylistSongViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("populate/", populate_view, name="populate"),
    # path("song/search/", search_songs, name="search_songs"),
    path("songs-search/", SongSearchView.as_view(), name="song-search"),
    path("artists-search/", ArtistSearchView.as_view(), name="artist-search"),
    path("albums-search/", AlbumSearchView.as_view(), name="album-search"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("user/like_song/", like_song, name="like_song"),
    path("user/unlike_song/", unlike_song, name="unlike_song"),
]
