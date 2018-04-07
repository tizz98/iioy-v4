from django.apps import AppConfig


class MoviesConfig(AppConfig):
    name = 'iioy.movies'

    def ready(self):
        from iioy.movies import signals  # noqa
