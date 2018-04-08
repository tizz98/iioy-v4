from typing import Type

from iioy.core.adapters import BaseAdapter
from iioy.core.interfaces import AdapterInterface, AdapterMethod
from iioy.movies.models import Genre


class GenreInterface(AdapterInterface):
    def __init__(self, adapter_cls: Type[BaseAdapter], external_id):
        self.external_id = external_id
        super().__init__(adapter_cls)

    def get_adapter(self):
        return self.adapter_cls(self.external_id)

    get_movies = AdapterMethod(default=list)
    get_genres = AdapterMethod(default=list)

    def save_genres(self):
        for genre in self.get_genres():
            Genre.objects.update_or_create(
                tmdb_id=genre.id,
                name=genre.name,
            )
