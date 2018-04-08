from django.db import models

from iioy.core.fields import SlugField
from iioy.core.models import BaseTmdbModel


class Movie(BaseTmdbModel):
    title = models.TextField()
    original_title = models.TextField()
    slug = SlugField(slug_field='title')

    tagline = models.TextField(null=True)
    budget = models.BigIntegerField(null=True)
    revenue = models.BigIntegerField(null=True)

    homepage = models.URLField(null=True)

    imdb_id = models.TextField()

    synopsis = models.TextField(null=True)
    runtime = models.IntegerField(null=True)  # in minutes
    mpaa_rating = models.TextField(null=True)

    release_date = models.DateField(null=True)

    backdrop_url = models.URLField(null=True)
    mobile_backdrop_url = models.URLField(null=True)

    poster_url = models.URLField(null=True)
    mobile_poster_url = models.URLField(null=True)

    trailer_url = models.URLField(null=True)

    genres = models.ManyToManyField(
        to='movies.Genre',
        related_name='movies',
    )
    similar_movies = models.ManyToManyField(to='self')

    class Meta:
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['imdb_id']),
        ]

    def __str__(self):
        return self.title

    def is_missing_data(self):
        return (
            self.synopsis is None
            or self.backdrop_url is None
            or not self.genres.exists()
        )
