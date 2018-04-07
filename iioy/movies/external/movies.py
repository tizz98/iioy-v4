import logging
from typing import Type

from iioy.movies.external.data_sources.base import BaseAdapter
from iioy.movies.models import Movie, Genre

logger = logging.getLogger(__name__)


class MovieMeta(type):
    def __new__(cls, name, bases, attributes):
        movie_cls = super().__new__(cls, name, bases, attributes)

        movie_methods = []

        for attr_name in attributes:
            attr = getattr(movie_cls, attr_name, None)

            if isinstance(attr, MovieMethod):
                movie_methods.append(attr_name)

        setattr(movie_cls, '_methods', movie_methods)
        return movie_cls


class MovieMethod:
    def __init__(self, default=None):
        self.default = default

        self.instance = None
        self.adapter = None
        self.attname = None

    def __call__(self, *args, **kwargs):
        try:
            return getattr(self.adapter, self.attname)(*args, **kwargs)
        except BaseAdapter.AdapterMethodError as err:
            logger.exception(f'Error calling method `{self.attname}`',
                             exc_info=err)
            return self.default

    def bind(self, instance: 'MovieInterface', attname: str):
        self.instance = instance
        self.adapter = self.instance.adapter
        self.attname = attname


class MovieInterface(metaclass=MovieMeta):
    """
    Examples
    --------
    >>> from iioy.movies.external import MovieInterface
    >>> from iioy.movies.external.data_sources import TmdbAdapter
    >>> movie = MovieInterface('354912', TmdbAdapter)
    >>> print(movie.get_title())
    >>> movie.save()
    """
    def __init__(self, external_id, adapter_cls: Type[BaseAdapter]):
        self.external_id = external_id
        self.adapter = adapter_cls(self.external_id)

        for attr_name in self._methods:
            attr = getattr(self, attr_name)
            attr.bind(self, attr_name)

    get_title = MovieMethod()
    get_original_title = MovieMethod()
    get_tagline = MovieMethod()
    get_budget = MovieMethod()
    get_revenue = MovieMethod()
    get_homepage = MovieMethod()
    get_imdb_id = MovieMethod()
    get_tmdb_id = MovieMethod()
    get_synopsis = MovieMethod()
    get_runtime = MovieMethod()
    get_mpaa_rating = MovieMethod()
    get_release_date = MovieMethod()
    get_backdrop_url = MovieMethod()
    get_mobile_backdrop_url = MovieMethod()
    get_poster_url = MovieMethod()
    get_mobile_poster_url = MovieMethod()
    get_trailer_url = MovieMethod()
    get_critics_rating = MovieMethod()
    get_audience_rating = MovieMethod()
    get_genres = MovieMethod()
    get_similar_movies = MovieMethod()

    def save(self):
        movie = self.build()
        movie.save()

        self.__set_genres(movie)
        self.__set_similar_movies(movie)

        return movie

    def build(self):
        data = dict(
            title=self.get_title(),
            original_title=self.get_original_title(),
            tagline=self.get_tagline(),
            budget=self.get_budget(),
            revenue=self.get_revenue(),
            homepage=self.get_homepage(),
            imdb_id=self.get_imdb_id(),
            tmdb_id=self.get_tmdb_id(),
            synopsis=self.get_synopsis(),
            runtime=self.get_runtime(),
            mpaa_rating=self.get_mpaa_rating(),
            release_date=self.get_release_date(),
            backdrop_url=self.get_backdrop_url(),
            mobile_backdrop_url=self.get_mobile_backdrop_url(),
            poster_url=self.get_poster_url(),
            mobile_poster_url=self.get_mobile_poster_url(),
            trailer_url=self.get_trailer_url(),
            critics_rating=self.get_critics_rating(),
            audience_rating=self.get_audience_rating(),
        )

        new_data = {}

        for key, value in data.items():
            if value is not None:
                new_data[key] = value

        return Movie.objects.update_or_create(**new_data)

    def __set_genres(self, movie: 'Movie'):
        genres = []
        for genre_data in self.get_genres():
            genres.append(Genre.objects.update_or_create(
                tmdb_id=genre_data.id,
                name=genre_data.name,
            ))

        movie.genres.set(genres, clear=True)

    def __set_similar_movies(self, movie: 'Movie'):
        similar = []
        for movie_data in self.get_similar_movies():
            similar.append(Movie.objects.update_or_create(
                tmdb_id=movie_data.id,
                title=movie_data.title,
                original_title=movie_data.original_title,
            ))

        movie.similar_movies.set(similar, clear=True)
