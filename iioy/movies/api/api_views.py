import logging

from django.http import Http404
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from iioy.movies.api.serializers import MovieSerializer
from iioy.movies.external.data_sources import TmdbMovieAdapter
from iioy.movies.external.errors import NoDataFoundError
from iioy.movies.external.movies import MovieInterface
from iioy.movies.models import Movie


logger = logging.getLogger(__name__)


class MovieViewInterface:
    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id

    def get_movie(self):
        try:
            return Movie.objects.get(tmdb_id=self.tmdb_id)
        except Movie.DoesNotExist:
            movie = MovieInterface(TmdbMovieAdapter, self.tmdb_id)

            try:
                return movie.save()
            except NoDataFoundError as err:
                logger.exception(f'Error finding {self.tmdb_id}',
                                 exc_info=err)
                raise Http404(f'Cannot find {self.tmdb_id}')


class MovieViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = 'tmdb_id'

    def get_object(self):
        interface = MovieViewInterface(self.kwargs[self.lookup_field])
        return interface.get_movie()
