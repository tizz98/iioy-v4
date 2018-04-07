import logging
from urllib.parse import urljoin

import tmdbsimple as tmdb

from iioy.core.adapters import UnImplementableMethod
from iioy.movies.external.data_sources.base import (
    BaseMovieAdapter, Genre, SimilarMovie,
    CastMember,
    BasePersonAdapter, BaseMovieCastAdapter, BaseMovieListAdapter, ListMovie)

logger = logging.getLogger(__name__)


class BaseTmdbAdapter:
    __config = {}

    tmdb_class = None

    def __init__(self, external_id):
        self.external_id = external_id
        self.tmdb_object = self.tmdb_class(self.external_id)

        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self.tmdb_object.info()
        return self._data

    @property
    def config(self):
        if not self.__config:
            self.__config = tmdb.Configuration().info()
        return self.__config

    def _get_image_url(self, path, size='original'):
        base = self.config['images']['secure_base_url']
        full_path = f'{size}/{path}'
        return urljoin(base, full_path)


class TmdbMovieAdapter(BaseMovieAdapter, BaseTmdbAdapter):
    tmdb_class = tmdb.Movies

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
        return self.__get_poster_url(self.data['poster_path'])

    def get_mobile_poster_url(self):
        return self.__get_mobile_poster_url(self.data['poster_path'])

    def get_trailer_url(self):
        logger.debug('Making additional request to TMDB for trailers.')

        trailers = list(filter(lambda t: t['site'].lower() == 'youtube',
                               self.tmdb_object.videos()['results']))

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

        def make_similar(data):
            poster_path = data['poster_path']
            return SimilarMovie(
                release_date=self.parse_date(data.pop('release_date')),
                poster_url=self.__get_poster_url(poster_path),
                mobile_poster_url=self.__get_mobile_poster_url(poster_path),
                **data,
            )

        similar = self.tmdb_object.similar_movies()
        return map(make_similar, similar['results'][:10])

    def __get_poster_url(self, path):
        return self._get_image_url(path, size='w780')

    def __get_mobile_poster_url(self, path):
        return self._get_image_url(path, size='w432')


class TmdbPersonAdapter(BasePersonAdapter, BaseTmdbAdapter):
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


class TmdbMovieCastAdapter(BaseMovieCastAdapter):
    person_adapter_cls = TmdbPersonAdapter

    def __init__(self, tmdb_movie_id):
        self.movie = tmdb.Movies(tmdb_movie_id)
        self.cast = self.movie.credits()['cast']

    def get_members(self):
        for member in self.cast:
            yield CastMember(
                id=member['cast_id'],
                person_id=member['id'],
                character_name=member['character'],
                order=member['order'],
            )


class TmdbMovieListAdapter(BaseMovieListAdapter):
    source = 'tmdb'
    movie_adapter_cls = TmdbMovieAdapter
    name = None
    list_func = None

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
