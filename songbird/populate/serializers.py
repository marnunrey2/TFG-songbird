from rest_framework import serializers
from .models import (
    Genre,
    Artist,
    Album,
    Song,
    Website,
    Playlist,
    Position,
    PlaylistSong,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class ArtistSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Album
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    main_artist = ArtistSerializer(read_only=True)
    collaborators = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = "__all__"


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class PlaylistSongSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    playlist = PlaylistSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = PlaylistSong
        fields = "__all__"
