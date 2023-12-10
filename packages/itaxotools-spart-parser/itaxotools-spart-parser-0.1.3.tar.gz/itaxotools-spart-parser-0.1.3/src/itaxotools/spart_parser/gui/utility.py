# -----------------------------------------------------------------------------
# Taxi3Gui - GUI for Taxi3
# Copyright (C) 2022  Patmanidis Stefanos
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

from PySide6 import QtCore

from dataclasses import dataclass
from typing import Callable, ClassVar, Optional, Union


class Property:
    key_ref = "properties"
    key_list = "_property_list"

    def __init__(self, type=object):
        self.type = type

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


class PropertyRef:
    def __init__(self, parent, key):
        self._parent = parent
        self._key = key

    @property
    def notify(self):
        return getattr(self._parent, Property.key_notify(self._key))

    @property
    def get(self):
        return getattr(self._parent, Property.key_getter(self._key))

    @property
    def set(self):
        return getattr(self._parent, Property.key_setter(self._key))

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self, value):
        return self.set(value)

    def update(self):
        self.notify.emit(self.get())


class PropertiesRef:
    def __init__(self, parent):
        self._parent = parent

    def __getattr__(self, attr):
        if attr in self._list():
            return PropertyRef(self._parent, attr)

    def __dir__(self):
        return super().__dir__() + self._list()

    def _list(self):
        return getattr(self._parent, Property.key_list)


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

    def _register_property(attrs, key, prop):
        key_value = Property.key_value(key)
        key_notify = Property.key_notify(key)
        key_getter = Property.key_getter(key)
        key_setter = Property.key_setter(key)
        key_list = Property.key_list

        notify = QtCore.Signal(prop.type)

        def getter(self):
            return getattr(self, key_value, None)

        def setter(self, value):
            old = getattr(self, key_value, None)
            setattr(self, key_value, value)
            if old != value:
                getattr(self, key_notify).emit(value)

        attrs[key_list].append(key)

        attrs[key_notify] = notify
        attrs[key_getter] = getter
        attrs[key_setter] = setter

        attrs[key] = QtCore.Property(
            type=prop.type,
            fget=getter,
            fset=setter,
            notify=notify,
        )

    def _add_ref(attrs):
        key_ref = Property.key_ref

        def getref(self):
            return PropertiesRef(self)

        attrs[key_ref] = property(getref)


@dataclass(frozen=True)
class Binding:
    bindings: ClassVar = dict()

    signal: QtCore.SignalInstance
    slot: Callable

    @classmethod
    def _bind(cls, signal, slot, proxy=None):
        if proxy:

            def proxy_slot(value):
                slot(proxy(value))

            bind_slot = proxy_slot
        else:
            bind_slot = slot
        signal.connect(bind_slot)
        id = cls(signal, slot)
        cls.bindings[id] = bind_slot
        return id

    @classmethod
    def _unbind(cls, signal, slot):
        id = cls(signal, slot)
        bind_slot = cls.bindings[id]
        signal.disconnect(bind_slot)


def bind(
    source: Union[PropertyRef, QtCore.SignalInstance],
    destination: Union[PropertyRef, Callable],
    proxy: Optional[Callable] = None,
):
    if isinstance(source, PropertyRef):
        signal = source.notify
    else:
        signal = source

    if isinstance(destination, PropertyRef):
        slot = destination.set
    else:
        slot = destination

    key = Binding._bind(signal, slot, proxy)
    if isinstance(source, PropertyRef):
        source.update()
    return key


def unbind(
    source: Union[PropertyRef, QtCore.SignalInstance],
    destination: Union[PropertyRef, Callable],
):
    if isinstance(source, PropertyRef):
        signal = source.notify
    else:
        signal = source

    if isinstance(destination, PropertyRef):
        slot = destination.set
    else:
        slot = destination

    return Binding._unbind(signal, slot)


class PropertyObject(QtCore.QObject, metaclass=PropertyMeta):
    pass
