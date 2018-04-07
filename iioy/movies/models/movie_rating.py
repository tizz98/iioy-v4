from django.db import models
from django_extensions.db.models import TimeStampedModel


class MovieRating(TimeStampedModel):
    source = models.TextField()
    value = models.TextField()

    movie = models.ForeignKey(
        to='movies.Movie',
        related_name='ratings',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.value} via {self.source} for {self.movie}'
