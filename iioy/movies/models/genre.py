from django.db import models

from iioy.core.models import BaseTmdbModel


class Genre(BaseTmdbModel):
    name = models.TextField()

    def __str__(self):
        return self.name
