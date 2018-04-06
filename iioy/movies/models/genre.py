from django.db import models
from django_extensions.db.models import TimeStampedModel


class Genre(TimeStampedModel):
    tmdb_id = models.TextField()
    name = models.TextField()

    def __str__(self):
        return self.name
