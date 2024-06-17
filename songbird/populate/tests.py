from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Song,
    UserSong,
    Artist,
    Album,
    Genre,
    Playlist,
    Website,
    Position,
    PlaylistSong,
)


class UserActionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            "testuser", "test@test.com", "testpassword"
        )
        self.test_user_profile = UserProfile.objects.create(user=self.test_user)
        artist = Artist.objects.create(name="test artist")
        self.test_song = Song.objects.create(name="test song", main_artist=artist)
        UserSong.objects.create(user=self.test_user_profile, song=self.test_song)

    def test_signup(self):
        response = self.client.post(
            "/api/signup/",
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "usertestpassword",
                "first_name": "New",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(UserProfile.objects.filter(user__username="newuser").exists())

    def test_login(self):
        response = self.client.post(
            "/api/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)

    def test_like_song(self):
        response = self.client.post(
            "/api/user/like_song/",
            {"user_id": self.test_user.id, "song_id": self.test_song.id},
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserSong.objects.filter(
                user=self.test_user_profile, song=self.test_song
            ).exists()
        )

    def test_unlike_song(self):
        response = self.client.post(
            "/api/user/unlike_song/",
            {"user_id": self.test_user.id, "song_id": self.test_song.id},
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            UserSong.objects.filter(
                user=self.test_user_profile, song=self.test_song
            ).exists()
        )

    def test_recommend_songs_view(self):
        response = self.client.get(f"/api/recommendations/{self.test_user.id}/")
        self.assertEqual(response.status_code, 200)


class ModelsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_artist = Artist.objects.create(name="test artist")
        self.test_song = Song.objects.create(
            name="test song", main_artist=self.test_artist
        )
        self.test_album = Album.objects.create(
            name="test album", artist=self.test_artist
        )
        self.test_genre = Genre.objects.create(name="test genre")
        self.test_website = Website.objects.create(name="test website")
        self.test_playlist = Playlist.objects.create(
            name="test playlist", website=self.test_website
        )
        position = Position.objects.create(position=1)
        PlaylistSong.objects.create(
            playlist=self.test_playlist, song=self.test_song, position=position
        )

    def test_song_search_view(self):
        response = self.client.get("/api/songs-search/", {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test song")

    def test_artist_search_view(self):
        response = self.client.get("/api/artists-search/", {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test artist")

    def test_album_search_view(self):
        response = self.client.get("/api/albums-search/", {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test album")

    def test_song_detail(self):
        response = self.client.get(f"/api/songs/{self.test_song.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test song")

    def test_artist_detail(self):
        response = self.client.get(f"/api/artists/{self.test_artist.name}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test artist")

    def test_artist_albums(self):
        response = self.client.get(f"/api/artists/{self.test_artist.name}/albums")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test album")

    def test_artist_songs(self):
        response = self.client.get(f"/api/artists/{self.test_artist.name}/songs")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test song")

    def test_album_detail(self):
        response = self.client.get(f"/api/albums/{self.test_album.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test album")

    def test_song_list(self):
        response = self.client.get("/api/songs/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test song")

    def test_artist_list(self):
        response = self.client.get("/api/artists/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test artist")

    def test_album_list(self):
        response = self.client.get("/api/albums/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test album")

    def test_genre_list(self):
        response = self.client.get("/api/genres/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test genre")

    def test_playlist_songs(self):
        response = self.client.get(
            f"/api/playlist_songs/{self.test_playlist.name}/{self.test_website.name}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test song")

    def test_website_names(self):
        response = self.client.get(f"/api/website_names/{self.test_playlist.name}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test website")


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            "testuser", "test@test.com", "testpassword"
        )
        self.test_song = Song.objects.create(name="test song")
        self.test_artist = Artist.objects.create(name="test artist")
        self.test_album = Album.objects.create(
            name="test album", artist=self.test_artist
        )
        self.test_playlist = Playlist.objects.create(name="test playlist")

    def test_admin_dashboard(self):
        response = self.client.get("/api/admin/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"num_users": 1')
        self.assertContains(response, '"num_songs": 1')
        self.assertContains(response, '"num_artists": 1')
        self.assertContains(response, '"num_albums": 1')
        self.assertContains(response, '"num_playlists": 1')
