from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db import IntegrityError
from django.db import transaction


class Genre(models.Model):
    BASE_GENRES = [
        "POP",
        "ROCK",
        "HIP HOP",
        "TRAP",
        "RAP",
        "REGGAETON",
        "URBAN",
        "LATIN",
        "BLUES",
        "METAL",
        "ALT",
        "COUNTRY",
        "SOUL",
        "PUNK",
        "FUNK",
        "FOLK",
        "HOUSE",
        "DANCE",
        "DISCO",
        "EDM",
        "TECHNO",
        "ELECTRO",
        "REGGAE",
        "AFR",
        "SALSA",
        "BACHATA",
        "FLAMENCO",
        "RUMBA",
        "JAPAN",
        "KOREAN",
        "CUMBIA",
        "R&B",
        "INDIE",
        "JAZZ",
        "CLASSICAL",
        "CHOIR",
        "INSTRUMENTAL",
        "SONGWRITER",
        "K-POP",
    ]

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    genres = models.ManyToManyField(Genre, blank=True)
    followers = models.JSONField(default=dict)
    images = models.CharField(max_length=255, null=True, blank=True)


class Album(models.Model):
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    total_tracks = models.IntegerField(null=True, blank=True)

    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="artist", null=True, blank=True
    )

    class Meta:
        unique_together = (
            "name",
            "artist",
        )


class Song(models.Model):

    PLATFORMS = [
        ("Spotify", "Spotify"),
        ("Amazon Music", "Amazon Music"),
        ("Deezer", "Deezer"),
        ("YouTube", "YouTube"),
        ("Apple Music", "Apple Music"),
    ]

    name = models.CharField(max_length=255)
    youtube_name = ArrayField(
        models.CharField(),
        default=list,
    )
    duration = models.IntegerField(null=True, blank=True)
    explicit = models.BooleanField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    available_at = ArrayField(
        models.CharField(
            choices=PLATFORMS,
        ),
        default=list,
    )
    date_added = models.DateTimeField(auto_now_add=True)
    reproductions = models.JSONField(default=dict)

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="album_songs",
        null=True,
        blank=True,
    )
    main_artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="main_artist",
        null=True,
        blank=True,
    )
    collaborators = models.ManyToManyField(Artist)

    class Meta:
        unique_together = (
            "name",
            "main_artist",
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure available_at and youtube_name does not contain duplicates
        self.youtube_name = list(set(self.youtube_name))
        self.available_at = list(set(self.available_at))
        super().save(*args, **kwargs)


class Website(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    website = models.ForeignKey(Website, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (
            "name",
            "website",
        )

    def __str__(self):
        return self.name


class Position(models.Model):
    position = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.position)


class PlaylistSong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="playlist_songs"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="playlist_position",
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    liked_songs = models.ManyToManyField(
        Song, blank=True, related_name="liked_by_users"
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                if (
                    self.user.email
                    and UserProfile.objects.filter(user__email=self.user.email)
                    .exclude(user__username=self.user.username)
                    .exists()
                ):
                    raise IntegrityError("Email addresses must be unique")
                self.user.save()
                super(UserProfile, self).save(*args, **kwargs)
        except IntegrityError as e:
            if "username" in str(e):
                raise IntegrityError("Username must be unique")
            raise e

    def __str__(self):
        return self.user.username
