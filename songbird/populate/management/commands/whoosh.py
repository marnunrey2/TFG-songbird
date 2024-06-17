import os
from django.core.management.base import BaseCommand
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from populate.models import Song, Artist, Album
from django.conf import settings
from rake_nltk import Rake
import nltk


def index_data():
    schema = Schema(
        id=ID(stored=True, unique=True),
        type=TEXT(stored=True),  # 'song', 'lyrics', 'artist', or 'album'
        content=TEXT(stored=True),
    )

    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)

    ix = create_in(settings.WHOOSH_INDEX, schema)
    writer = ix.writer()

    # Initialize RAKE
    rake = Rake()

    # Index songs
    for song in Song.objects.all():
        writer.add_document(id=f"song_{song.id}", type="song", content=song.name)

        if not song.lyrics:
            continue

        # Extract keywords from lyrics
        rake.extract_keywords_from_text(song.lyrics)
        keywords = " ".join(rake.get_ranked_phrases()[:5])
        writer.add_document(id=f"lyrics_{song.id}", type="lyrics", content=keywords)

    # Index artists
    for artist in Artist.objects.all():
        writer.add_document(
            id=f"artist_{artist.name}", type="artist", content=artist.name
        )

    # Index albums
    for album in Album.objects.all():
        writer.add_document(id=f"album_{album.id}", type="album", content=album.name)

    writer.commit()


class Command(BaseCommand):
    help = "Index data for Whoosh search"

    nltk.download("stopwords")
    nltk.download("punkt")

    def handle(self, *args, **kwargs):
        index_data()
        self.stdout.write(self.style.SUCCESS("Successfully indexed data"))
