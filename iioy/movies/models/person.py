from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Person(TimeStampedModel):
    tmdb_id = models.TextField()

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

    class Meta:
        indexes = [
            models.Index(fields=['tmdb_id']),
        ]
