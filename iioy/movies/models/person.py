from django.contrib.postgres.fields import ArrayField
from django.db import models

from iioy.core.models import BaseTmdbModel


class Person(BaseTmdbModel):
    name = models.TextField()
    profile_picture_url = models.URLField()
    biography = models.TextField(null=True)

    day_of_birth = models.DateField(null=True)
    day_of_death = models.DateField(null=True)

    homepage = models.URLField(null=True)
    birthplace = models.TextField(null=True)

    aliases = ArrayField(
        models.TextField(),
        default=list,
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['tmdb_id']),
        ]
