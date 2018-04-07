from operator import attrgetter

from django.db import models
from django_extensions.db.models import TimeStampedModel

from iioy.core.managers import TmdbManagerFactory


class BaseTmdbModel(TimeStampedModel):
    tmdb_id = models.TextField()

    objects = TmdbManagerFactory()

    class Meta:
        abstract = True

    def update(self, other: 'BaseTmdbModel'):
        for field in self.get_field_names() - {'id', 'pk'}:
            other_value = getattr(other, field)

            if other_value is not None:
                setattr(self, field, other_value)

        self.save()

    def get_field_names(self):
        return set(map(attrgetter('attname'), self._meta.fields))
