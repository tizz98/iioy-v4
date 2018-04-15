import abc
from collections import namedtuple

from dateutil.parser import parse


class BaseAdapter(abc.ABC):
    class AdapterMethodError(Exception):
        pass

    @staticmethod
    def parse_date(date):
        if not date:
            return None
        return parse(date).date()

    @staticmethod
    def get_youtube_url(key):
        return f'https://youtube.com/embed/{key}'

    @property
    @abc.abstractmethod
    def source(self):
        pass


class UnImplementableMethod:
    def __init__(self, message):
        self.message = message

    def __call__(self, *args, **kwargs):
        raise BaseAdapter.AdapterMethodError(self.message)


class SmartTuple:
    def __init__(self, *args, **kwargs):
        self.namedtuple = namedtuple(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict) and not kwargs:
            kwargs = args[0]

        new_kwargs = {}

        for k, v in kwargs.items():
            if k in self.namedtuple._fields:
                new_kwargs[k] = v

        return self.namedtuple(**new_kwargs)
