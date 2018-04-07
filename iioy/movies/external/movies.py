from typing import Type

from iioy.core.adapters import BaseAdapter
from iioy.core.interfaces import AdapterInterface, AdapterMethod
from iioy.movies.models import Movie, Genre


class MovieInterface(AdapterInterface):
    """
    Examples
    --------
    >>> from iioy.movies.external.movies import MovieInterface
    >>> from iioy.movies.external.data_sources import TmdbMovieAdapter
    >>> movie = MovieInterface(TmdbMovieAdapter, '354912')
    >>> print(movie.get_title())
    >>> movie.save()
    """
    def __init__(self, adapter_cls: Type[BaseAdapter], external_id):
        self.external_id = external_id

        super().__init__(adapter_cls)

    def get_adapter(self):
        return self.adapter_cls(self.external_id)

    get_title = AdapterMethod()
    get_original_title = AdapterMethod()
    get_tagline = AdapterMethod()
    get_budget = AdapterMethod()
    get_revenue = AdapterMethod()
    get_homepage = AdapterMethod()
    get_imdb_id = AdapterMethod()
    get_tmdb_id = AdapterMethod()
    get_synopsis = AdapterMethod()
    get_runtime = AdapterMethod()
    get_mpaa_rating = AdapterMethod()
    get_release_date = AdapterMethod()
    get_backdrop_url = AdapterMethod()
    get_mobile_backdrop_url = AdapterMethod()
    get_poster_url = AdapterMethod()
    get_mobile_poster_url = AdapterMethod()
    get_trailer_url = AdapterMethod()
    get_critics_rating = AdapterMethod()
    get_audience_rating = AdapterMethod()
    get_genres = AdapterMethod()
    get_similar_movies = AdapterMethod()

    def save(self):
        movie = Movie.objects.update_or_create(**self.get_movie_data())

        self.__set_genres(movie)
        self.__set_similar_movies(movie)

        return movie

    def build(self):
        return Movie(**self.get_movie_data())

    def get_movie_data(self):
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

        return new_data

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
