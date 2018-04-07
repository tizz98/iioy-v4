from iioy.core.interfaces import AdapterInterface, AdapterMethod
from iioy.movies.external.movies import MovieInterface
from iioy.movies.external.data_sources.base import ListAdapterMeta
from iioy.movies.models import MovieList


class ListInterface(AdapterInterface):
    """
    Examples
    --------
    >>> from iioy.movies.external.lists import ListInterface
    >>> movie_list = ListInterface('tmdb', 'Popular')
    >>> movie_list.save()
    """
    def __init__(self, source: str, name: str):
        self.source = source
        self.name = name

        super().__init__(ListAdapterMeta.lists[self.source][self.name])

    def get_adapter(self):
        return self.adapter_cls()

    get_name = AdapterMethod()
    get_movies = AdapterMethod()

    def save(self):
        new_movies = []

        for movie_data in self.get_movies():
            movie = MovieInterface(
                adapter_cls=self.adapter.movie_adapter_cls,
                external_id=movie_data.id,
            )
            new_movies.append(movie.save())

        movie_list, _ = MovieList.objects.get_or_create(
            name=self.get_name(),
            source=self.source,
        )
        movie_list.movies.set(new_movies, clear=True)
