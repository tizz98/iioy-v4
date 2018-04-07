import abc

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
