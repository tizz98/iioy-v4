from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from iioy.movies import tasks
from iioy.movies.external.cast_members import MovieCastMembersInterface
from iioy.movies.external.data_sources.tmdb import TmdbMovieCastAdapter
from iioy.movies.models import Movie


@receiver(post_save, sender=Movie)
def create_cast_members(instance: Movie, **kwargs):
    cast = MovieCastMembersInterface(TmdbMovieCastAdapter, instance.tmdb_id)
    # todo: do in parallel with celery
    # cast.save()


@receiver(post_save, sender=Movie)
def update_ratings(instance: Movie, **kwargs):
    # todo: queue celery task
    if not instance.mpaa_rating and instance.tmdb_id and instance.imdb_id:
        transaction.on_commit(lambda: tasks.update_ratings(
            instance.tmdb_id,
            instance.imdb_id
        ))
