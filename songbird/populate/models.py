from django.db import models


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
    ]

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    genres = models.ManyToManyField(Genre, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    href = models.CharField(max_length=255, null=True, blank=True)


class Album(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    total_tracks = models.IntegerField(null=True, blank=True)
    href = models.CharField(max_length=255, null=True, blank=True)

    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="artist", null=True, blank=True
    )

    class Meta:
        unique_together = (
            "name",
            "artist",
        )


class Song(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(null=True, blank=True)
    explicit = models.BooleanField(null=True, blank=True)
    spotify_streams = models.BigIntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    href = models.CharField(max_length=255, null=True, blank=True)
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
