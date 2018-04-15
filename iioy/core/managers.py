from django.db.models import QuerySet


def TmdbManagerFactory(lookup_field='tmdb_id'):
    def get_lookup(kwargs):
        return {lookup_field: kwargs[lookup_field]}

    class TmdbQuerySet(QuerySet):
        def update_or_create(self, **kwargs):
            try:
                existing = self.get(**get_lookup(kwargs))
                existing.update(self.model(**kwargs))
                return existing
            except self.model.MultipleObjectsReturned:
                existing = self.filter(**get_lookup(kwargs)).latest('created')

                (
                    self
                    .filter(**get_lookup(kwargs))
                    .exclude(pk=existing.pk)
                    .delete()
                )

                existing.update(self.model(**kwargs))
                return existing
            except self.model.DoesNotExist:
                return self.create(**kwargs)

    return TmdbQuerySet.as_manager()
