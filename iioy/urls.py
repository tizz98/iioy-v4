from django.urls import path, include

urlpatterns = [
    path('api/', include('iioy.movies.api.api_urls')),
]
