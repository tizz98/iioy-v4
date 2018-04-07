import abc
import logging
from typing import Type

from iioy.movies.external.data_sources.base import BaseAdapter


logger = logging.getLogger(__name__)


class InterfaceMeta(abc.ABCMeta):
    def __new__(cls, name, bases, attributes):
        new_cls = super().__new__(cls, name, bases, attributes)

        methods = []

        for attr in attributes:
            method = getattr(new_cls, attr, None)

            if isinstance(method, InterfaceMethod):
                methods.append(attr)

        setattr(new_cls, '_methods', methods)
        return new_cls


class InterfaceMethod(abc.ABC):
    def __init__(self):
        self.instance = None
        self.attname = None

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def bind(self, instance: 'BaseInterface', attname: str):
        self.instance = instance
        self.attname = attname


class BaseInterface(metaclass=InterfaceMeta):
    def __init__(self):
        for attr in self._methods:
            method = getattr(self, attr)
            method.bind(self, attr)


class AdapterInterface(BaseInterface):
    def __init__(self, adapter_cls: Type[BaseAdapter]):
        self.adapter_cls = adapter_cls
        self.adapter = self.get_adapter()

        super().__init__()

    @abc.abstractmethod
    def get_adapter(self):
        pass


class AdapterMethod(InterfaceMethod):
    def __init__(self, default=None):
        super().__init__()

        self.default = default
        self.adapter = None

    def __call__(self, *args, **kwargs):
        try:
            return getattr(self.adapter, self.attname)(*args, **kwargs)
        except BaseAdapter.AdapterMethodError as err:
            logger.exception(f'Error calling method `{self.attname}`',
                             exc_info=err)
            return self.default

    def bind(self, instance: 'AdapterInterface', attname: str):
        super().bind(instance, attname)
        self.adapter = self.instance.adapter
