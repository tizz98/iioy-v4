import logging
from urllib.parse import urljoin

import requests
import tmdbsimple as tmdb
from requests import HTTPError

from iioy.core.adapters import UnImplementableMethod
from iioy.movies.external.data_sources.base import (
    BaseMovieAdapter, Genre, SimpleMovie, CastMember,
    BasePersonAdapter, BaseMovieCastAdapter, BaseMovieListAdapter, ListMovie,
    BaseGenreAdapter, TmdbMovie,
)
from iioy.movies.external.errors import NotFoundHardError, HardError

logger = logging.getLogger(__name__)


class BaseTmdbAdapter:
    __config = {}

    source = 'tmdb'
    tmdb_class = None

    def __init__(self, external_id):
        self.external_id = external_id
        self.tmdb_object = self.tmdb_class(self.external_id)

        self._data = None

    @property
    def data(self):
        if self._data is None:
            try:
                self._data = self.tmdb_object.info()
            except HTTPError as error:
                status_code = getattr(error.response, 'status_code')
                if status_code == requests.codes.not_found:
                    raise NotFoundHardError('Not found')
                elif status_code == requests.codes.too_many_requests:
                    raise HardError('Rate limited')
        return self._data

    @property
    def config(self):
        if not self.__config:
            self.__config = tmdb.Configuration().info()
        return self.__config

    def _get_image_url(self, path, size='original'):
        if not path:
            return None

        base = self.config['images']['secure_base_url']
        full_path = f'{size}/{path}'
        return urljoin(base, full_path)

    def _get_poster_url(self, path):
        return self._get_image_url(path, size='w780')

    def _get_mobile_poster_url(self, path):
        return self._get_image_url(path, size='w432')


class TmdbMovieAdapter(BaseTmdbAdapter, BaseMovieAdapter):
    tmdb_class = tmdb.Movies
    similar_movie_limit = 10

    def get_title(self):
        return self.data['title']

    def get_original_title(self):
        return self.data['original_title']

    def get_tagline(self):
        return self.data['tagline']

    def get_budget(self):
        return self.data['budget']

    def get_revenue(self):
        return self.data['revenue']

    def get_homepage(self):
        return self.data['homepage']

    def get_imdb_id(self):
        return self.data['imdb_id']

    def get_tmdb_id(self):
        return self.data['id']

    def get_synopsis(self):
        return self.data['overview']

    def get_runtime(self):
        return self.data['runtime']

    get_mpaa_rating = UnImplementableMethod('TMDB does not provide MPAA ratings.')  # noqa: E501

    def get_release_date(self):
        return self.parse_date(self.data['release_date'])

    def get_backdrop_url(self):
        return self._get_image_url(self.data['backdrop_path'])

    def get_mobile_backdrop_url(self):
        return self._get_image_url(self.data['backdrop_path'], size='w1280')

    def get_poster_url(self):
        return self._get_poster_url(self.data['poster_path'])

    def get_mobile_poster_url(self):
        return self._get_mobile_poster_url(self.data['poster_path'])

    def get_trailer_url(self):
        logger.debug('Making additional request to TMDB for trailers.')

        videos = self.tmdb_object.videos()['results']
        trailers = list(filter(lambda t: t['site'].lower() == 'youtube', videos))  # noqa: E501

        if len(trailers) > 0:
            trailer = trailers[0]
            return self.get_youtube_url(trailer['key'])
        return None

    get_ratings = UnImplementableMethod(
        'This method is deprecated for TMDB, '
        'use Rotten tomatoes or OMDB.')

    def get_genres(self):
        return map(Genre, self.data['genres'])

    def get_similar_movies(self):
        logger.debug('Making additional request to TMDB for similar movies')

        movies = self.tmdb_object.similar_movies()['results']

        for data in movies[:self.similar_movie_limit]:
            poster_path = data['poster_path']

            yield SimpleMovie(
                release_date=self.parse_date(data.pop('release_date')),
                poster_url=self._get_poster_url(poster_path),
                mobile_poster_url=self._get_mobile_poster_url(poster_path),
                **data,
            )

    def search(self, query):
        for result in tmdb.Search().movie(query=query)['results']:
            poster_path = result['poster_path']

            yield TmdbMovie(
                release_date=self.parse_date(result.pop('release_date')),
                poster_url=self._get_poster_url(poster_path),
                mobile_poster_url=self._get_mobile_poster_url(poster_path),
                tmdb_id=result['id'],
                **result
            )


class TmdbPersonAdapter(BaseTmdbAdapter, BasePersonAdapter):
    tmdb_class = tmdb.People

    def get_tmdb_id(self):
        return self.data['id']

    def get_name(self):
        return self.data['name']

    def get_profile_picture_url(self):
        return self._get_image_url(self.data['profile_path'], size='h632')

    def get_biography(self):
        return self.data['biography']

    def get_day_of_birth(self):
        return self.parse_date(self.data.get('birthday'))

    def get_day_of_death(self):
        return self.parse_date(self.data.get('deathday'))

    def get_homepage(self):
        return self.data.get('homepage')

    def get_birthplace(self):
        return self.data.get('place_of_birth')

    def get_aliases(self):
        return self.data['also_known_as']


class TmdbMovieCastAdapter(BaseTmdbAdapter, BaseMovieCastAdapter):
    source = 'tmdb'
    person_adapter_cls = TmdbPersonAdapter
    tmdb_class = tmdb.Movies

    def get_members(self):
        cast = self.tmdb_object.credits()['cast']

        for member in cast:
            yield CastMember(
                id=member['cast_id'],
                person_id=member['id'],
                character_name=member['character'],
                order=member['order'],
            )


class TmdbMovieListAdapter(BaseTmdbAdapter, BaseMovieListAdapter):
    source = 'tmdb'
    movie_adapter_cls = TmdbMovieAdapter
    tmdb_class = tmdb.Movies
    name = None
    list_func = None

    def __init__(self):
        super().__init__(None)

    def get_name(self):
        return self.name

    def get_movies(self):
        for movie in getattr(tmdb.Movies(), self.list_func)()['results']:
            yield ListMovie(**movie)


class NowPlayingListAdapter(TmdbMovieListAdapter):
    list_func = 'now_playing'
    name = 'Now playing'


class PopularListAdapter(TmdbMovieListAdapter):
    list_func = 'popular'
    name = 'Popular'


class TopRatedListAdapter(TmdbMovieListAdapter):
    list_func = 'top_rated'
    name = 'Top rated'


class UpcomingListAdapter(TmdbMovieListAdapter):
    list_func = 'upcoming'
    name = 'Upcoming'


class TmdbGenreAdapter(BaseTmdbAdapter, BaseGenreAdapter):
    tmdb_class = tmdb.Genres

    def get_genres(self):
        for data in self.tmdb_object.movie_list()['genres']:
            yield Genre(**data)

    def get_movies(self):
        for data in self.tmdb_object.movies()['results']:
            poster_path = data['poster_path']

            yield TmdbMovie(
                tmdb_id=data['id'],
                release_date=self.parse_date(data.pop('release_date')),
                poster_url=self._get_poster_url(poster_path),
                mobile_poster_url=self._get_mobile_poster_url(poster_path),
                **data,
            )
