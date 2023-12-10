# -----------------------------------------------------------------------------
# Commons - Utility classes for iTaxoTools modules
# Copyright (C) 2021-2023  Patmanidis Stefanos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from __future__ import annotations

from PySide6 import QtCore

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from types import UnionType
from typing import Callable, Iterator, Optional, TypeVar, Union, get_origin

from .utility import AttrDict


class Instance:
    """Pass as type or instance to instantiate a property by default"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class _Instance:
    """Internal instructions for default class instatiation"""

    def __init__(self, type, *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs


class Property:
    key_ref = "properties"
    key_list = "_property_list"
    key_tags = "_property_tags"

    def __init__(self, type=object, default=None, tag=None):
        if isinstance(type, UnionType):
            type = object
        self.type = type
        self.default = default
        self.tag = tag

    @staticmethod
    def key_value(key):
        return f"_property_{key}_value"

    @staticmethod
    def key_notify(key):
        return f"_property_{key}_notify"

    @staticmethod
    def key_getter(key):
        return f"_property_{key}_getter"

    @staticmethod
    def key_setter(key):
        return f"_property_{key}_setter"

    @staticmethod
    def key_default(key):
        return f"_property_{key}_default"


class PropertyRef:
    def __init__(self, parent, key):
        self._parent = parent
        self._key = key

    @property
    def notify(self) -> Callable[[], None]:
        return getattr(self._parent, Property.key_notify(self._key))

    @property
    def get(self) -> Callable[[], object]:
        return getattr(self._parent, Property.key_getter(self._key))

    @property
    def set(self) -> Callable[[object], None]:
        return getattr(self._parent, Property.key_setter(self._key))

    @property
    def default(self) -> object:
        default = getattr(self._parent, Property.key_default(self._key))
        if isinstance(default, _Instance):
            return default.type(*default.args, **default.kwargs)
        return default

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> object:
        return self.get()

    @property
    def tag(self) -> object:
        tags = getattr(self._parent, Property.key_tags)
        return tags[self._key]

    @value.setter
    def value(self, value):
        return self.set(value)

    def update(self) -> Callable[[], object]:
        self.notify.emit(self.get())


class PropertiesRef:
    def __init__(self, parent):
        self._parent = parent

    def __getattr__(self, attr):
        if attr in self._list():
            return PropertyRef(self._parent, attr)
        raise AttributeError(
            f"{repr(type(self._parent).__name__)} has no property: {repr(attr)}"
        )

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __dir__(self):
        return super().__dir__() + self._list()

    def _list(self):
        return getattr(self._parent, Property.key_list)

    def __iter__(self) -> Iterator[PropertyRef]:
        return (self[key] for key in self._list())

    def __contains__(self, key):
        return key in self._list()


class PropertyMeta(type(QtCore.QObject)):
    def __new__(cls, name, bases, attrs):
        properties = {
            key: attrs[key] for key in attrs if isinstance(attrs[key], Property)
        }
        cls._init_list(bases, attrs)
        for key, prop in properties.items():
            cls._register_property(attrs, key, prop)
        cls._add_ref(attrs)
        obj = super().__new__(cls, name, bases, attrs)
        return obj

    def _init_list(bases, attrs):
        key_list = Property.key_list
        lists = [getattr(base, key_list, []) for base in bases]
        attrs[key_list] = sum(lists, [])

        key_tags = Property.key_tags
        attrs[key_tags] = defaultdict(lambda: None)

    def _register_property(attrs: dict[str, object], key: str, prop: Property):
        key_value = Property.key_value(key)
        key_notify = Property.key_notify(key)
        key_getter = Property.key_getter(key)
        key_setter = Property.key_setter(key)
        key_default = Property.key_default(key)
        key_list = Property.key_list
        key_tags = Property.key_tags

        if prop.tag is not None:
            attrs[key_tags][key] = prop.tag

        prop_type = get_origin(prop.type) or prop.type
        if isinstance(prop_type, TypeVar) and prop_type.__bound__:
            prop_type = prop_type.__bound__

        notify = QtCore.Signal(prop_type)

        def getter(self):
            return getattr(self, key_value, None)

        def setter(self, value):
            old = getattr(self, key_value, None)
            setattr(self, key_value, value)
            if old != value:
                getattr(self, key_notify).emit(value)

        default = prop.default
        if default == Instance:
            default = _Instance(prop_type)
        if isinstance(default, Instance):
            default = _Instance(prop_type, *default.args, **default.kwargs)

        attrs[key_list].append(key)

        attrs[key_notify] = notify
        attrs[key_getter] = getter
        attrs[key_setter] = setter
        attrs[key_default] = default

        attrs[key] = QtCore.Property(
            type=prop_type,
            fget=getter,
            fset=setter,
            notify=notify,
        )

    def _add_ref(attrs):
        key_ref = Property.key_ref

        def getref(self):
            return PropertiesRef(self)

        attrs[key_ref] = property(getref)


class PropertyObject(QtCore.QObject, metaclass=PropertyMeta):
    properties: PropertiesRef

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property_defaults()

    def _set_property_defaults(self):
        for property in self.properties:
            property.set(property.default)

    def as_dict(self):
        return AttrDict({property.key: property.value for property in self.properties})


class EnumObjectMeta(PropertyMeta):
    def __new__(cls, name, bases, attrs):
        enum = attrs.get("enum", None)
        if not enum:
            return super().__new__(cls, name, bases, attrs)

        get_key = attrs.get("get_key", lambda x: x.key)
        get_type = attrs.get("get_type", lambda x: x.type)
        get_default = attrs.get("get_default", lambda x: x.default)
        for field in enum:
            attrs[get_key(field)] = Property(get_type(field), get_default(field))
        return super().__new__(cls, name, bases, attrs)


class EnumObject(PropertyObject, metaclass=EnumObjectMeta):
    enum: Enum

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "enum" in dir(self):
            self.reset()

    def reset(self):
        self._set_property_defaults()


BindingHash = tuple[QtCore.SignalInstance, Callable]


@dataclass(frozen=True)
class Binding:
    source: Union[PropertyRef, QtCore.SignalInstance]
    destination: Union[PropertyRef, Callable]
    signal: QtCore.SignalInstance
    slot: Callable
    bound_slot: Callable
    update_slot: Callable

    def __post_init__(self):
        self.update()

    @staticmethod
    def _get_proxied_slot(slot, proxy):
        if not proxy:
            return slot

        def proxy_slot(value):
            slot(proxy(value))

        return proxy_slot

    @staticmethod
    def _get_conditional_slot(slot, condition):
        if not condition:
            return slot

        def conditional_slot(value):
            if condition(value):
                slot(value)

        return conditional_slot

    @classmethod
    def new(
        cls,
        source: Union[PropertyRef, QtCore.SignalInstance],
        destination: Union[PropertyRef, Callable],
        proxy: Optional[Callable] = None,
        condition: Optional[Callable] = None,
    ) -> Binding:
        if isinstance(source, PropertyRef):
            signal = source.notify
            update_slot = source.update
        else:
            signal = source
            update_slot = None

        if isinstance(destination, PropertyRef):
            slot = destination.set
        else:
            slot = destination

        bound_slot = slot
        bound_slot = cls._get_proxied_slot(bound_slot, proxy)
        bound_slot = cls._get_conditional_slot(bound_slot, condition)

        signal.connect(bound_slot)

        return cls(
            source=source,
            destination=destination,
            signal=signal,
            slot=slot,
            bound_slot=bound_slot,
            update_slot=update_slot,
        )

    def unbind(self):
        self.signal.disconnect(self.bound_slot)

    def update(self):
        if self.update_slot is not None:
            self.update_slot()


class Binder(dict[BindingHash, Binding]):
    def bind(
        self,
        source: Union[PropertyRef, QtCore.SignalInstance],
        destination: Union[PropertyRef, Callable],
        proxy: Optional[Callable] = None,
        condition: Optional[Callable] = None,
    ) -> None:
        binding = Binding.new(source, destination, proxy, condition)
        self[self._hash(source, destination)] = binding

    def unbind(
        self,
        source: Union[PropertyRef, QtCore.SignalInstance],
        destination: Union[PropertyRef, Callable],
    ) -> None:
        hash = self._hash(source, destination)
        self[hash].unbind()
        del self[hash]

    def unbind_all(self):
        for binding in self.values():
            binding.unbind()
        self.clear()

    def update(self):
        for binding in self.values():
            binding.update()

    def _hash(
        self,
        source: Union[PropertyRef, QtCore.SignalInstance],
        destination: Union[PropertyRef, Callable],
    ) -> BindingHash:
        if isinstance(source, PropertyRef):
            signal = source.notify
        else:
            signal = source

        if isinstance(destination, PropertyRef):
            slot = destination.set
        else:
            slot = destination

        return (signal, slot)
