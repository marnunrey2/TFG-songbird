from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=20, blank=True)
    image = models.URLField(blank=True)
    concerts = models.JSONField(blank=True, null=True)
    followers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=50)
    release_date = models.DateField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    artist = models.ForeignKey(
        "Artist", on_delete=models.CASCADE, related_name="albums"
    )

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=50)
    release_date = models.CharField(blank=True, null=True)
    position = models.CharField(blank=True, null=True)
    duration = models.CharField(blank=True, null=True)
    explicit = models.BooleanField(default=False)
    image = models.CharField(blank=True)

    """
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="songs")
    collaborators = models.ManyToManyField(
        "Artist", related_name="collaborations", blank=True
    )
    album = models.ForeignKey("Album", on_delete=models.SET_NULL, null=True, blank=True)
    """

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
