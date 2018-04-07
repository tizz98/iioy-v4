from django.db import transaction

from iioy.movies.external.data_sources.omdb import OmdbMovieAdapter
from iioy.movies.external.movies import MovieInterface


def update_ratings(tmdb_id, imdb_id):
    with transaction.atomic():
        movie = MovieInterface(
            OmdbMovieAdapter,
            tmdb_id,
            imdb_id,
        )
        movie.save()
