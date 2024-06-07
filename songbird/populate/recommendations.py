from collections import Counter
from .models import UserSong, Song
from .serializers import SongSerializer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from django.conf import settings


def recommend_songs(user):
    res = []
    liked_songs = UserSong.objects.filter(user=user).select_related("song")

    if liked_songs:
        # Extract keywords for liked songs
        liked_song_ids = [song.song.id for song in liked_songs]
        liked_song_keywords = extract_keywords_from_index(liked_song_ids)

        # Extract keywords for all songs
        all_songs = Song.objects.all()
        all_song_ids = [song.id for song in all_songs]
        all_song_keywords = extract_keywords_from_index(all_song_ids)

        # Calculate similarities
        similarities = compute_similarities(
            all_song_keywords, liked_song_keywords.values()
        )

        # Get top recommendations
        top_recommendations = Counter(similarities).most_common(20)

        for song_id, score in top_recommendations:
            if not liked_songs.filter(song__id=song_id).exists():
                song_instance = Song.objects.get(id=song_id)
                res.append(
                    {"song": SongSerializer(song_instance).data, "score": 100 * score}
                )

    return res


def extract_keywords_from_index(song_ids):
    ix = open_dir(settings.WHOOSH_INDEX)
    keywords = {}
    with ix.searcher() as searcher:
        for song_id in song_ids:
            query = QueryParser("id", ix.schema).parse(f"lyrics_{song_id}")
            results = searcher.search(query, limit=1)
            if results:
                keywords[song_id] = set(results[0]["content"].split())
    return keywords


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))


def compute_similarities(song_keywords, liked_song_keywords):
    similarities = {}
    for song_id, song_kw in song_keywords.items():
        max_similarity = 0
        for liked_kw in liked_song_keywords:
            similarity = dice_coefficient(song_kw, liked_kw)
            if similarity > max_similarity:
                max_similarity = similarity
        similarities[song_id] = max_similarity
    return similarities
