from django.urls import path, include

from iioy.core.views import HealthCheck

urlpatterns = [
    path('.health-check/', HealthCheck.as_view(), name='health'),
    path('api/', include('iioy.movies.api.api_urls')),
]
