from operator import attrgetter

from django.db import models
from django_extensions.db.models import TimeStampedModel

from iioy.core.fields import SlugField
from iioy.core.managers import TmdbManagerFactory


class Movie(TimeStampedModel):
    title = models.TextField()
    original_title = models.TextField()
    slug = SlugField(slug_field='title')

    tagline = models.TextField(null=True)
    budget = models.TextField(null=True)
    revenue = models.TextField(null=True)

    homepage = models.URLField(null=True)

    imdb_id = models.TextField()
    tmdb_id = models.TextField()

    synopsis = models.TextField(null=True)
    runtime = models.TextField(null=True)
    mpaa_rating = models.TextField(null=True)

    release_date = models.DateField(null=True)

    backdrop_url = models.TextField(null=True)
    mobile_backdrop_url = models.TextField(null=True)

    poster_url = models.TextField(null=True)
    mobile_poster_url = models.TextField(null=True)

    trailer_url = models.TextField(null=True)

    critics_rating = models.TextField(null=True)
    audience_rating = models.TextField(null=True)

    genres = models.ManyToManyField(
        to='movies.Genre',
        related_name='movies',
    )
    similar_movies = models.ManyToManyField(to='self')

    objects = TmdbManagerFactory()

    class Meta:
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['imdb_id']),
        ]

    def __str__(self):
        return self.title

    def update(self, other: 'Movie'):
        for field in self.get_field_names() - {'id', 'pk'}:
            other_value = getattr(other, field)

            if other_value is not None:
                setattr(self, field, other_value)

        self.save()

    def get_field_names(self):
        return set(map(attrgetter('attname'), self._meta.fields))
