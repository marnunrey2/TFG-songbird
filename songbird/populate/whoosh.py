from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC, BOOLEAN, DATETIME
from datetime import datetime, time
from .models import (
    Song,
    Artist,
    Album,
)
import os
import json


def create_whoosh_index():

    # Ensure directory exists
    if not os.path.exists("indexwhoosh"):
        os.mkdir("indexwhoosh")

    create_whoosh_index_songs()
    create_whoosh_index_artists()
    create_whoosh_index_albums()


def create_whoosh_index_songs():
    # Define schema
    song_schema = Schema(
        name=TEXT(stored=True),
        youtube_name=TEXT(stored=True),
        duration=NUMERIC(stored=True),
        explicit=BOOLEAN(stored=True),
        release_date=DATETIME(stored=True),
        images=TEXT(stored=True),
        lyrics=TEXT(stored=True),
        available_at=TEXT(stored=True),
        reproductions=TEXT(stored=True),
        album=TEXT(stored=True),
        album_images=TEXT(stored=True),
        main_artist=TEXT(stored=True),
        collaborators=TEXT(stored=True),
    )

    # Ensure directory exists
    if not os.path.exists("indexwhoosh/song"):
        os.mkdir("indexwhoosh/song")

    # Create index
    index = create_in("indexwhoosh/song", song_schema)

    # Add data to index
    writer = index.writer()
    for song in Song.objects.all():
        release_date = (
            datetime.combine(song.release_date, time.min) if song.release_date else None
        )
        reproductions = json.dumps(song.reproductions) if song.reproductions else ""
        album = song.album.name if song.album else ""
        main_artist = song.main_artist.name if song.main_artist else ""
        collaborators = ", ".join([artist.name for artist in song.collaborators.all()])

        writer.add_document(
            name=song.name,
            youtube_name=", ".join(song.youtube_name),
            duration=song.duration,
            explicit=song.explicit,
            release_date=release_date,
            images=song.images,
            lyrics=song.lyrics,
            available_at=", ".join(song.available_at),
            reproductions=reproductions,
            album=album,
            album_images=song.album.images if song.album else "",
            main_artist=main_artist,
            collaborators=collaborators,
        )
    writer.commit()


def create_whoosh_index_artists():
    # Define schema
    artist_schema = Schema(
        name=TEXT(stored=True),
        genres=TEXT(stored=True),
        followers=TEXT(stored=True),
        images=TEXT(stored=True),
    )

    # Ensure directory exists
    if not os.path.exists("indexwhoosh/artist"):
        os.mkdir("indexwhoosh/artist")

    # Create index
    index = create_in("indexwhoosh/artist", artist_schema)

    # Add data to index
    writer = index.writer()
    for artist in Artist.objects.all():
        genres = ", ".join([genre.name for genre in artist.genres.all()])
        followers = json.dumps(artist.followers) if artist.followers else ""

        writer.add_document(
            name=artist.name,
            genres=genres,
            followers=followers,
            images=artist.images,
        )
    writer.commit()


def create_whoosh_index_albums():
    # Define schema
    albums_schema = Schema(
        name=TEXT(stored=True),
        genre=TEXT(stored=True),
        images=TEXT(stored=True),
        release_date=DATETIME(stored=True),
        total_tracks=NUMERIC(stored=True),
        artist=TEXT(stored=True),
    )

    # Ensure directory exists
    if not os.path.exists("indexwhoosh/album"):
        os.mkdir("indexwhoosh/album")

    # Create index
    index = create_in("indexwhoosh/album", albums_schema)

    # Add data to index
    writer = index.writer()
    for album in Album.objects.all():
        genres = ", ".join([genre.name for genre in album.genre.all()])
        release_date = (
            datetime.combine(album.release_date, time.min)
            if album.release_date
            else None
        )

        writer.add_document(
            name=album.name,
            genre=genres,
            images=album.images,
            release_date=release_date,
            total_tracks=album.total_tracks,
            artist=album.artist.name,
        )
    writer.commit()
