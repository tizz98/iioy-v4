from django.core.management import BaseCommand

from iioy.movies.external.data_sources.base import ListAdapterMeta
from iioy.movies.external.data_sources.tmdb import TmdbGenreAdapter
from iioy.movies.external.genres import GenreInterface
from iioy.movies.external.lists import ListInterface


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-lists',
            '-s',
            action='store_true',
            dest='skip_lists',
            help='Skip creating movie lists.',
        )

    def handle(self, *args, **options):
        if not options['skip_lists']:
            self.create_movie_lists()

        self.create_genres()

    def create_movie_lists(self):
        print('Creating movie lists')

        for list_source in ListAdapterMeta.lists.keys():
            print(f'--> {list_source}')

            for name in ListAdapterMeta.lists[list_source].keys():
                print(f'----> {name}')

                movie_list = ListInterface(list_source, name)
                movie_list.save()

    def create_genres(self):
        print('Creating Genres')
        interface = GenreInterface(TmdbGenreAdapter, None)
        interface.save_genres()
