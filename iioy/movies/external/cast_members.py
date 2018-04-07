from typing import Type

from iioy.core.adapters import BaseAdapter
from iioy.core.interfaces import AdapterInterface, AdapterMethod
from iioy.movies.external.people import PersonInterface
from iioy.movies.models import CastMember, Movie


class MoveCastMembersInterface(AdapterInterface):
    def __init__(self, adapter_cls: Type[BaseAdapter], external_movie_id):
        self.external_movie_id = external_movie_id

        super().__init__(adapter_cls)

    def get_adapter(self):
        return self.adapter_cls(self.external_movie_id)

    get_members = AdapterMethod()

    def save(self):
        cast_members = self.get_members()
        movie = Movie.objects.get(tmdb_id=self.external_movie_id)

        saved = []

        for member in cast_members:
            person = PersonInterface(
                adapter_cls=self.adapter_cls.person_adapter_cls,
                external_id=member.person_id,
            )
            person = person.save()

            saved.append(CastMember.objects.update_or_create(
                character_name=member.character_name,
                person=person,
                movie=movie,
                order=member.order,
            ))

        return saved
