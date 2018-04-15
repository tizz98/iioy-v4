from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from iioy.movies import tasks
from iioy.movies.models import Movie


@receiver(post_save, sender=Movie)
def update_ratings(instance: Movie, **kwargs):
    should_update_ratings = (
        not instance.mpaa_rating
        and instance.tmdb_id
        and instance.imdb_id
    )
    if should_update_ratings:
        transaction.on_commit(lambda: tasks.update_ratings.delay(
            instance.tmdb_id,
            instance.imdb_id
        ))
