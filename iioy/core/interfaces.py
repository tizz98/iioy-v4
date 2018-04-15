import abc
import logging
from typing import Type

from iioy.movies.external.data_sources.base import BaseAdapter
from iioy.movies.external.errors import HardError

logger = logging.getLogger(__name__)


class InterfaceMethod(abc.ABC):
    def __init__(self, instance=None, attname=None):
        self.instance = instance
        self.attname = attname

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def bind(self, instance: 'BaseInterface', attname: str):
        return self.__class__(instance, attname)


class BaseInterface:
    def __init__(self):
        for attr in self._methods:
            method = getattr(self, attr)
            setattr(self, attr, method.bind(self, attr))

    @property
    def _methods(self):
        methods = []

        for attr in set(dir(self)) - {'_methods'}:
            method = getattr(self, attr)

            if isinstance(method, InterfaceMethod):
                methods.append(attr)

        return methods


class AdapterInterface(BaseInterface):
    def __init__(self, adapter_cls: Type[BaseAdapter]):
        self.adapter_cls = adapter_cls
        self.adapter = self.get_adapter()

        super().__init__()

    @abc.abstractmethod
    def get_adapter(self):
        pass


class AdapterMethod(InterfaceMethod):
    def __init__(self, instance=None, attname=None, default=None):
        super().__init__(instance, attname)

        self._default = default
        self.adapter = None

    @property
    def default(self):
        if callable(self._default):
            return self._default()
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    def __call__(self, *args, **kwargs):
        try:
            return getattr(self.adapter, self.attname)(*args, **kwargs)
        except BaseAdapter.AdapterMethodError as err:
            logger.debug(f'Error calling method `{self.attname}`',
                         exc_info=err)
            return self.default
        except HardError as e:
            raise e
        except Exception as e:
            logger.exception(f'Error calling method `{self.attname}`',
                             exc_info=e)
            return self.default

    def bind(self, instance: 'AdapterInterface', attname: str):
        new = super().bind(instance, attname)
        new.adapter = new.instance.adapter
        new.default = self._default
        return new
