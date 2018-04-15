from celery import group
from django.db import transaction
from django.db.models import Q, Count
from django.utils import timezone

from iioy.celery import app
from iioy.movies.external.cast_members import MovieCastMembersInterface
from iioy.movies.external.data_sources.base import ListAdapterMeta
from iioy.movies.external.data_sources.omdb import OmdbMovieAdapter
from iioy.movies.external.data_sources.tmdb import (
    TmdbGenreAdapter,
    TmdbMovieAdapter,
    TmdbMovieCastAdapter,
)
from iioy.movies.external.genres import GenreInterface
from iioy.movies.external.lists import ListInterface
from iioy.movies.external.movies import MovieInterface
from iioy.movies.models import Movie


@app.task(rate_limit='2/s', ignore_result=True)
@transaction.atomic
def update_ratings(tmdb_id, imdb_id):
    movie = MovieInterface(OmdbMovieAdapter, tmdb_id, imdb_id)
    movie.save()


@app.task(rate_limit='1/s', ignore_result=True)
@transaction.atomic
def update_movie(tmdb_id):
    movie = MovieInterface(TmdbMovieAdapter, tmdb_id)
    movie.save()


@app.task(rate_limit='1/s', ignore_result=True)
@transaction.atomic
def create_cast_members(tmdb_id):
    cast = MovieCastMembersInterface(TmdbMovieCastAdapter, tmdb_id)
    cast.save()


@app.task(ignore_result=True)
@transaction.atomic
def update_genres():
    interface = GenreInterface(TmdbGenreAdapter, None)
    interface.save_genres()


@app.task(rate_limit='1/m', ignore_result=True)
@transaction.atomic
def update_movie_list(list_source, name):
    movie_list = ListInterface(list_source, name)
    movie_list.save()


@app.task(ignore_result=True)
def update_movie_lists():
    tasks = []

    for list_source in ListAdapterMeta.lists.keys():
        for name in ListAdapterMeta.lists[list_source].keys():
            tasks.append(update_movie_list.si(list_source, name))

    group(tasks)()


@app.task(ignore_result=True)
def update_missing_data_movies():
    tasks = []

    for tmdb_id in Movie.objects.annotate(
        genre_count=Count('genres'),
    ).filter(
        Q(synopsis=None) |
        Q(backdrop_url=None) |
        Q(genre_count__lte=0),
        tmdb_id__isnull=False,
    ).values_list('tmdb_id', flat=True).iterator():
        tasks.append(update_movie.si(tmdb_id))

    group(tasks)()


@app.task(ignore_result=True)
def update_missing_ratings():
    tasks = []

    for tmdb_id, imdb_id in Movie.objects.annotate(
        ratings_count=Count('ratings'),
    ).filter(
        ratings_count__lte=0,
        release_date__lte=timezone.now().date(),
        tmdb_id__isnull=False,
        imdb_id__isnull=False,
    ).values_list('tmdb_id', 'imdb_id').iterator():
        tasks.append(update_ratings.si(tmdb_id, imdb_id))

    group(tasks)()
