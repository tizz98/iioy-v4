from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet


def TmdbManagerFactory(lookup_field='tmdb_id'):
    class TmdbQuerySet(QuerySet):
        def update_or_create(self, **kwargs):
            try:
                existing = self.get(**{lookup_field: kwargs[lookup_field]})
                existing.update(self.model(**kwargs))
                return existing
            except ObjectDoesNotExist:
                return self.create(**kwargs)

    return TmdbQuerySet.as_manager()
