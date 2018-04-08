import logging

from django.http import Http404
from rest_framework import mixins, response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from iioy.movies.api.serializers import (
    MovieSerializer, SimpleMovieSerializer,
    SimpleMovieListSerializer, DetailedMovieListSerializer
)
from iioy.movies.external.data_sources import TmdbMovieAdapter
from iioy.movies.external.data_sources.tmdb import TmdbGenreAdapter
from iioy.movies.external.errors import NoDataFoundError
from iioy.movies.external.genres import GenreInterface
from iioy.movies.external.movies import MovieInterface
from iioy.movies.models import Movie, MovieList, Genre

logger = logging.getLogger(__name__)


class MovieViewInterface:
    adapter_cls = TmdbMovieAdapter

    def __init__(self, tmdb_id=None, query=None):
        self.tmdb_id = tmdb_id
        self.query = query
        self.interface = MovieInterface(self.adapter_cls, self.tmdb_id)

    def get_movie(self):
        try:
            movie = Movie.objects.get(tmdb_id=self.tmdb_id)

            if movie.is_missing_data():
                return self.__save()
            return movie
        except Movie.DoesNotExist:
            try:
                return self.__save()
            except NoDataFoundError as err:
                logger.exception(f'Error finding {self.tmdb_id}',
                                 exc_info=err)
                raise Http404(f'Cannot find {self.tmdb_id}')

    def search(self):
        return self.interface.search(self.query)

    def __save(self):
        return self.interface.save()


class GenreViewInterface:
    movies_to_show = 20
    adapter_cls = TmdbGenreAdapter

    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.interface = GenreInterface(self.adapter_cls, self.tmdb_id)

    def get_movies(self):
        try:
            if self.__get_movies().count() < self.movies_to_show:
                return self.interface.get_movies()
            return self.__get_movies().order_by('?')[:self.movies_to_show]
        except Genre.DoesNotExist:
            return self.interface.get_movies()

    def get_name(self):
        try:
            return self.__get_name()
        except Genre.DoesNotExist:
            self.interface.save_genres()
            return self.__get_name()

    def __get_name(self):
        genre = self.__get_genre()
        return genre.name

    def __get_genre(self):
        return Genre.objects.get(tmdb_id=self.tmdb_id)

    def __get_movies(self):
        return self.__get_genre().movies.all()


class MovieViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = 'tmdb_id'

    def get_object(self):
        interface = MovieViewInterface(self.kwargs[self.lookup_field])
        return interface.get_movie()


class MovieSearchApi(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        query = self.request.GET.get('q')

        if not query:
            return response.Response(data=[])

        interface = MovieViewInterface(query=query)
        serializer = SimpleMovieSerializer(interface.search(), many=True)
        return response.Response(data=serializer.data)


class MovieGenreApi(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        genre_id = self.kwargs['tmdb_id']
        interface = GenreViewInterface(genre_id)
        serializer = SimpleMovieSerializer(interface.get_movies(), many=True)

        return response.Response(data={
            'id': genre_id,
            'name': interface.get_name(),
            'movies': serializer.data,
        })


class MovieListViewSet(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    queryset = MovieList.objects.all().order_by('name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedMovieListSerializer
        return SimpleMovieListSerializer
