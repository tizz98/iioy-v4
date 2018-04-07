import abc
from collections import defaultdict

from iioy.core.adapters import SmartTuple, BaseAdapter

Genre = SmartTuple('Genre', [
    'id',
    'name'
])
SimilarMovie = SmartTuple('SimilarMovie', [
    'id',
    'title',
    'original_title',
])
CastMember = SmartTuple('CastMember', [
    'id',
    'person_id',
    'character_name',
    'order',
])
ListMovie = SmartTuple('ListMovie', [
    'id',
    'title',
    'original_title',
])


class BaseMovieAdapter(BaseAdapter):
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


class BasePersonAdapter(BaseAdapter):
    @abc.abstractmethod
    def get_tmdb_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_profile_picture_url(self):
        pass

    @abc.abstractmethod
    def get_biography(self):
        pass

    @abc.abstractmethod
    def get_day_of_birth(self):
        pass

    @abc.abstractmethod
    def get_day_of_death(self):
        pass

    @abc.abstractmethod
    def get_homepage(self):
        pass

    @abc.abstractmethod
    def get_birthplace(self):
        pass

    @abc.abstractmethod
    def get_aliases(self):
        pass


class BaseMovieCastAdapter(BaseAdapter):
    person_adapter_cls = None

    @abc.abstractmethod
    def get_members(self):
        pass


class ListAdapterMeta(abc.ABCMeta):
    lists = defaultdict(dict)

    def __new__(cls, name, bases, attributes):
        new_cls = super().__new__(cls, name, bases, attributes)

        if bases[0] == BaseAdapter:
            return new_cls

        if new_cls.name is not None:
            cls.lists[new_cls.source][new_cls.name] = new_cls
        return new_cls


class BaseMovieListAdapter(BaseAdapter, metaclass=ListAdapterMeta):
    @property
    @abc.abstractmethod
    def source(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def movie_adapter_cls(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_movies(self):
        pass
