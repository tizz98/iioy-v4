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


class MovieViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = 'tmdb_id'

    def get_object(self):
        try:
            return super().get_object()
        except Http404 as e:
            tmdb_id = self.kwargs[self.lookup_field]
            movie = MovieInterface(TmdbMovieAdapter, tmdb_id)

            try:
                return movie.save()
            except NoDataFoundError as err:
                logger.exception(f'Error finding {tmdb_id}',
                                 exc_info=err)
                raise e
