from django.urls import path
from rest_framework.routers import SimpleRouter

from iioy.movies.api import api_views

router = SimpleRouter()
router.register('movies', api_views.MovieViewSet)
router.register('lists', api_views.MovieListViewSet)

urlpatterns = [
    path('movies/search/',
         api_views.MovieSearchApi.as_view(),
         name='movie-search'),
    path('genres/<int:tmdb_id>/',
         api_views.MovieGenreApi.as_view(),
         name='genre-detail'),
] + router.urls
