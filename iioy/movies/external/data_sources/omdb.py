import omdb
from django.conf import settings

from iioy.core.adapters import UnImplementableMethod
from iioy.movies.external.data_sources.base import BaseMovieAdapter, \
    MovieRating

client = omdb.OMDBClient(apikey=settings.OMDB_API_KEY)


class OmdbMovieAdapter(BaseMovieAdapter):
    """
    NB: The OMDB api has many of these fields, but we rely on TMDB as the
    source of truth and only use OMDB as supplemental.
    """
    def __init__(self, tmdb_id, imdb_id):
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id

        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = client.get(imdbid=self.imdb_id)
        return self._data

    get_title = UnImplementableMethod('Not used from OMDB.')
    get_original_title = UnImplementableMethod('Not used from OMDB.')
    get_tagline = UnImplementableMethod('Not used from OMDB.')
    get_budget = UnImplementableMethod('Not used from OMDB.')
    get_revenue = UnImplementableMethod('Not used from OMDB.')
    get_homepage = UnImplementableMethod('Not used from OMDB.')

    def get_imdb_id(self):
        return self.imdb_id

    def get_tmdb_id(self):
        return self.tmdb_id

    get_synopsis = UnImplementableMethod('Not used from OMDB.')
    get_runtime = UnImplementableMethod('Not used from OMDB.')

    def get_mpaa_rating(self):
        return self.data['rated']

    get_release_date = UnImplementableMethod('Not used from OMDB.')
    get_backdrop_url = UnImplementableMethod('Not used from OMDB.')
    get_mobile_backdrop_url = UnImplementableMethod('Not used from OMDB.')
    get_poster_url = UnImplementableMethod('Not used from OMDB.')
    get_mobile_poster_url = UnImplementableMethod('Not used from OMDB.')
    get_trailer_url = UnImplementableMethod('Not used from OMDB.')

    def get_ratings(self):
        for rating in self.data['ratings']:
            yield MovieRating(tmdb_id=self.tmdb_id, **rating)

    get_genres = UnImplementableMethod('Not used from OMDB.')
    get_similar_movies = UnImplementableMethod('Not used from OMDB.')
    search = UnImplementableMethod('Not used from OMDB.')
