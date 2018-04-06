from django.db import models
from django_extensions.db.models import TimeStampedModel


class CastMember(TimeStampedModel):
    character_name = models.TextField(null=True)

    person = models.ForeignKey(
        to='movies.Person',
        related_name='roles',
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        to='movies.Movie',
        related_name='cast_members',
        on_delete=models.CASCADE,
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.character_name} ({self.person})'
