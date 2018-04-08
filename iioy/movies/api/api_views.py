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
from iioy.movies.external.errors import NoDataFoundError
from iioy.movies.external.movies import MovieInterface
from iioy.movies.models import Movie, MovieList

logger = logging.getLogger(__name__)


class MovieViewInterface:
    adapter_cls = TmdbMovieAdapter

    def __init__(self, tmdb_id=None, query=None):
        self.tmdb_id = tmdb_id
        self.query = query
        self.interface = MovieInterface(self.adapter_cls, self.tmdb_id)

    def get_movie(self):
        try:
            return Movie.objects.get(tmdb_id=self.tmdb_id)
        except Movie.DoesNotExist:
            try:
                return self.interface.save()
            except NoDataFoundError as err:
                logger.exception(f'Error finding {self.tmdb_id}',
                                 exc_info=err)
                raise Http404(f'Cannot find {self.tmdb_id}')

    def search(self):
        return self.interface.search(self.query)


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
