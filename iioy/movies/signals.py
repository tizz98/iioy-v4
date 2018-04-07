from django.db.models.signals import post_save
from django.dispatch import receiver

from iioy.movies.external.cast_members import MovieCastMembersInterface
from iioy.movies.external.data_sources.tmdb import TmdbMovieCastAdapter
from iioy.movies.models import Movie


@receiver(post_save, sender=Movie)
def create_cast_members(instance, **kwargs):
    cast = MovieCastMembersInterface(TmdbMovieCastAdapter, instance.tmdb_id)
    # todo: do in parallel with celery
    # cast.save()
