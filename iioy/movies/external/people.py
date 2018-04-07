from typing import Type

from iioy.core.adapters import BaseAdapter
from iioy.core.interfaces import AdapterInterface, AdapterMethod
from iioy.movies.models import Person


class PersonInterface(AdapterInterface):
    def __init__(self, adapter_cls: Type[BaseAdapter], external_id):
        self.external_id = external_id

        super().__init__(adapter_cls)

    def get_adapter(self):
        return self.adapter_cls(self.external_id)

    get_tmdb_id = AdapterMethod()
    get_name = AdapterMethod()
    get_profile_picture_url = AdapterMethod()
    get_biography = AdapterMethod()
    get_day_of_birth = AdapterMethod()
    get_day_of_death = AdapterMethod()
    get_homepage = AdapterMethod()
    get_birthplace = AdapterMethod()
    get_aliases = AdapterMethod()

    def save(self):
        return Person.objects.update_or_create(**self.get_person_data())

    def build(self):
        return Person(**self.get_person_data())

    def get_person_data(self):
        return dict(
            tmdb_id=self.get_tmdb_id(),
            name=self.get_name(),
            profile_picture_url=self.get_profile_picture_url(),
            biography=self.get_biography(),
            day_of_birth=self.get_day_of_birth(),
            day_of_death=self.get_day_of_death(),
            homepage=self.get_homepage(),
            birthplace=self.get_birthplace(),
            aliases=self.get_aliases(),
        )
