from django.db import models
from django_extensions.db.models import TimeStampedModel

from iioy.core.fields import SlugField


class MovieList(TimeStampedModel):
    name = models.TextField()
    slug = SlugField(slug_field='name')

    movies = models.ManyToManyField('movies.Movie')

    def __str__(self):
        return self.name
