from rest_framework.routers import SimpleRouter

from iioy.movies.api import api_views

router = SimpleRouter()
router.register('movies', api_views.MovieViewSet)

urlpatterns = [] + router.urls
