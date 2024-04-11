from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


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
    popularity = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
    href = models.CharField(max_length=255, null=True, blank=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="songs", null=True, blank=True
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


class Playlist(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
