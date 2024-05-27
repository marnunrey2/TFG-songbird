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
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
]
