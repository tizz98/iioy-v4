import abc
from collections import namedtuple

from dateutil.parser import parse


class BaseAdapter(abc.ABC):
    class AdapterMethodError(Exception):
        def __init__(self, message: str, adapter: 'BaseAdapter'):
            super().__init__(message)
            self.adapter = adapter

    @staticmethod
    def parse_date(date):
        if date is None:
            return None
        return parse(date)


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
