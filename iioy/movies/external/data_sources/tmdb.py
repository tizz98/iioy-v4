import logging
from urllib.parse import urljoin

import tmdbsimple as tmdb

from iioy.movies.external.data_sources.base import BaseAdapter, Genre, \
    SimilarMovie

logger = logging.getLogger(__name__)


class TmdbAdapter(BaseAdapter):
    __config = {}

    def __init__(self, external_id):
        super().__init__(external_id)

        self.movie = tmdb.Movies(self.external_id)
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self.movie.info()
        return self._data

    @property
    def config(self):
        if not self.__config:
            self.__config = tmdb.Configuration().info()
        return self.__config

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

    def get_mpaa_rating(self):
        raise self.AdapterMethodError(
            message='TMDB does not provide MPAA ratings.',
            adapter=self,
        )

    def get_release_date(self):
        return self.parse_date(self.data['release_date'])

    def get_backdrop_url(self):
        return self.__get_image_url(self.data['backdrop_path'])

    def get_mobile_backdrop_url(self):
        return self.__get_image_url(self.data['backdrop_path'], size='w1280')

    def get_poster_url(self):
        return self.__get_image_url(self.data['poster_path'], size='w780')

    def get_mobile_poster_url(self):
        return self.__get_image_url(self.data['poster_path'], size='w432')

    def get_trailer_url(self):
        raise self.AdapterMethodError(
            message='TMDB does not provide trailers.',
            adapter=self,
        )

    def get_critics_rating(self):
        raise self.AdapterMethodError(
            message='This method is deprecated for TMDB, use Rotten tomatoes.',
            adapter=self,
        )

    def get_audience_rating(self):
        raise self.AdapterMethodError(
            message='This method is deprecated for TMDB, use Rotten tomatoes.',
            adapter=self,
        )

    def get_genres(self):
        return map(Genre, self.data['genres'])

    def get_similar_movies(self):
        logger.debug('Making additional request to TMDB for similar movies')

        similar = self.movie.similar_movies()
        return map(SimilarMovie, similar['results'][:10])

    def __get_image_url(self, path, size='original'):
        base = self.config['images']['secure_base_url']
        return urljoin(urljoin(base, size), path)
