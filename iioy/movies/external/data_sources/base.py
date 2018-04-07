import abc
from collections import namedtuple

from dateutil.parser import parse


class SmartTuple:
    def __init__(self, *args, **kwargs):
        self.namedtuple = namedtuple(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict) and not kwargs:
            kwargs = args[0]

        new_kwargs = {}

        for k, v in kwargs.items():
            if k in self.namedtuple._fields:
                new_kwargs[k] = v

        return self.namedtuple(**new_kwargs)


Genre = SmartTuple('Genre', [
    'id',
    'name'
])
SimilarMovie = SmartTuple('SimilarMovie', [
    'id',
    'title',
    'original_title',
])


class BaseAdapter(abc.ABC):
    class AdapterMethodError(Exception):
        def __init__(self, message: str, adapter: 'BaseAdapter'):
            super().__init__(message)
            self.adapter = adapter

    def __init__(self, external_id):
        self.external_id = external_id

    @abc.abstractmethod
    def get_title(self):
        pass

    @abc.abstractmethod
    def get_original_title(self):
        pass

    @abc.abstractmethod
    def get_tagline(self):
        pass

    @abc.abstractmethod
    def get_budget(self):
        pass

    @abc.abstractmethod
    def get_revenue(self):
        pass

    @abc.abstractmethod
    def get_homepage(self):
        pass

    @abc.abstractmethod
    def get_imdb_id(self):
        pass

    @abc.abstractmethod
    def get_tmdb_id(self):
        pass

    @abc.abstractmethod
    def get_synopsis(self):
        pass

    @abc.abstractmethod
    def get_runtime(self):
        pass

    @abc.abstractmethod
    def get_mpaa_rating(self):
        pass

    @abc.abstractmethod
    def get_release_date(self):
        pass

    @abc.abstractmethod
    def get_backdrop_url(self):
        pass

    @abc.abstractmethod
    def get_mobile_backdrop_url(self):
        pass

    @abc.abstractmethod
    def get_poster_url(self):
        pass

    @abc.abstractmethod
    def get_mobile_poster_url(self):
        pass

    @abc.abstractmethod
    def get_trailer_url(self):
        pass

    @abc.abstractmethod
    def get_critics_rating(self):
        pass

    @abc.abstractmethod
    def get_audience_rating(self):
        pass

    @abc.abstractmethod
    def get_genres(self):
        pass

    @abc.abstractmethod
    def get_similar_movies(self):
        pass

    @staticmethod
    def parse_date(date):
        return parse(date)
