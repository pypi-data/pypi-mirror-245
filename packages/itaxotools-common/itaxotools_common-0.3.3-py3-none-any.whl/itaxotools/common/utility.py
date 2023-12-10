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

"""Utility classes and functions"""


from typing import Callable, Generic, TypeVar

KeyType = TypeVar("KeyType")
DecoratedType = TypeVar("DecoratedType")


class DecoratorDict(Generic[KeyType, DecoratedType]):
    """
    Instances can be used as decorators that accept a single key as argument.
    Decorated functions can then be accessed by key.
    """

    def __init__(self):
        self.items = dict()

    def __call__(self, key: KeyType) -> Callable[[DecoratedType], DecoratedType]:
        def decorator(func: DecoratedType) -> DecoratedType:
            self.items[key] = func
            return func

        return decorator

    def __getitem__(self, key: KeyType) -> DecoratedType:
        if key not in self.items:
            raise Exception("")
        return self.items[key]

    def __contains__(self, key) -> bool:
        return key in self.items

    def __iter__(self) -> iter:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)


class AttrDict(dict):
    """Members can also be accessed as attributes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __iter__(self):
        return iter(self.values())


class Guard:
    """Should probably use threading.Lock"""

    def __init__(self):
        self.locked = False

    def __enter__(self):
        self.locked = True

    def __exit__(self, type, value, trace):
        self.locked = False

    def __bool__(self):
        return self.locked


def override(f: DecoratedType) -> DecoratedType:
    return f


def type_convert(value, type, default):
    try:
        return type(value)
    except ValueError:
        return default


def human_readable_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1000.0 or unit == "GB":
            break
        size /= 1000.0
    return f"{size:.2f} {unit}"


def human_readable_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    segments = [
        f'{int(h)} hour{"s" if h >= 2 else ""}' if h else None,
        f'{int(m)} minute{"s" if m >= 2 else ""}' if m else None,
        f"{s:.2f} seconds" if s else None,
    ]
    segments = (x for x in segments if x)
    return ", ".join(segments)
