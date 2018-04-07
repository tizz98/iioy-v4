from django.core.management import BaseCommand

from iioy.movies.external.data_sources.base import ListAdapterMeta
from iioy.movies.external.lists import ListInterface


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating movie lists')

        for list_source in ListAdapterMeta.lists.keys():
            print(f'--> {list_source}')

            for name in ListAdapterMeta.lists[list_source].keys():
                print(f'----> {name}')

                movie_list = ListInterface(list_source, name)
                movie_list.save()
