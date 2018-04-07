from rest_framework import serializers

from iioy.movies.models import Movie, Genre


class SimpleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        read_only_fields = (
            'tmdb_id',
            'name',
        )
        fields = read_only_fields


class SimpleMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        read_only_fields = (
            'tmdb_id',
            'title',
            'slug',
            'release_date',
            'poster_url',
            'mobile_poster_url',
        )
        fields = read_only_fields


class MovieSerializer(serializers.ModelSerializer):
    genres = SimpleGenreSerializer(many=True)
    similar_movies = SimpleMovieSerializer(many=True)

    class Meta:
        model = Movie
        read_only_fields = (
            'tmdb_id',
            'title',
            'original_title',
            'slug',
            'tagline',
            'budget',
            'revenue',
            'homepage',
            'imdb_id',
            'synopsis',
            'runtime',
            'mpaa_rating',
            'release_date',
            'backdrop_url',
            'mobile_backdrop_url',
            'poster_url',
            'mobile_poster_url',
            'trailer_url',
            'critics_rating',
            'audience_rating',
            'genres',
            'similar_movies',
        )
        fields = read_only_fields
