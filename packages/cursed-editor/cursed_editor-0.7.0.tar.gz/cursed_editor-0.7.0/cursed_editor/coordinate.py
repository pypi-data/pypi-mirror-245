#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Philip Zerull

# This file is part of "The Cursed Editor"

# "The Cursed Editor" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

from .immutable import Immutable


class Coordinate(Immutable):
    x = 0
    y = 0

    def __repr__(self) -> str:
        return f"<Coordinate x={self.x}, y={self.y}>"

    def __add__(self, other: "Coordinate") -> "Coordinate":
        if not isinstance(other, Coordinate):
            raise TypeError("Can only add Coordinates to Coordinates")
        return Coordinate(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        if not isinstance(other, Coordinate):
            raise TypeError("Can only subtract Coordinates from Coordinates")
        return Coordinate(x=self.x - other.x, y=self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            raise TypeError("can only compare Coordinates to other Coordinates")
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            raise TypeError("can only compare Coordinates to other Coordinates")
        return (self.y > other.y) or (self.y == other.y and self.x > other.x)

    def __ge__(self, other: object) -> bool:
        return (self == other) or (self > other)


Coordinate.__doc__ = """
    A Coordinate object is used to represent the x and y coordinates of
    a two dimantional integer based grid.
"""

Coordinate.__init__.__doc__ = """
    Create a new Coordinate using integer values for x and y

    >>> Coordinate(x=1, y=2)
    <Coordinate x=1, y=2>
"""

Coordinate.__eq__.__doc__ = """
    Compares two Coordinate objects for equality.  Coordinates are
    equal if both the x and y components are the same
    >>> Coordinate(x=1, y=2) == Coordinate(x=1, y=2)
    True

    >>> Coordinate(x=1, y=2) == Coordinate(x=0, y=2)
    False

    >>> Coordinate(x=1, y=2) == Coordinate(x=1, y=0)
    False

    >>> Coordinate(x=1, y=2) == Coordinate(x=-1, y=-2)
    False

    This will raise a type error if attempting to compare a Coordinate
    to something other than a Coordinate.

    >>> Coordinate(x=1, y=2) == 5
    Traceback (most recent call last):
    TypeError: can only compare Coordinates to other Coordinates
"""

Coordinate.__gt__.__doc__ = """
    Checks if this Coordinate is greater than the other Coordiante.

    >>> Coordinate(x=5, y=5) > Coordinate(x=2, y=2)
    True

    >>> Coordinate(x=5, y=5) > Coordinate(x=2, y=5)
    True

    >>> Coordinate(x=50, y=5) > Coordinate(x=2, y=5)
    True

    >>> Coordinate(x=0, y=50) > Coordinate(x=2, y=5)
    True

    This will raise a type error if attempting to compare a Coordinate
    to something other than a Coordinate.

    >>> Coordinate(x=1, y=2) > 5
    Traceback (most recent call last):
    TypeError: can only compare Coordinates to other Coordinates
"""

Coordinate.__ge__.__doc__ = """
    Checks if this Coordinate is greater than or equal to the other Coordiante.

    >>> Coordinate(x=5, y=5) >= Coordinate(x=2, y=2)
    True

    >>> Coordinate(x=5, y=5) >= Coordinate(x=5, y=5)
    True


    This will raise a type error if attempting to compare a Coordinate
    to something other than a Coordinate.

    >>> Coordinate(x=1, y=2) >= 5
    Traceback (most recent call last):
    TypeError: can only compare Coordinates to other Coordinates
"""

Coordinate.__add__.__doc__ = """
    Adds two Coordinate objects together to produce a new one.
    >>> Coordinate(x=1, y=2) + Coordinate(x=4, y=8)
    <Coordinate x=5, y=10>

    This will raise a type error if attempting to add something
    other than a coordinate.

    >>> Coordinate(x=1, y=2) + 5
    Traceback (most recent call last):
    TypeError: Can only add Coordinates to Coordinates
"""

Coordinate.__sub__.__doc__ = """
    Subtracts two Coordinate objets together to produce a new one.
    >>> Coordinate(x=100, y=200) - Coordinate(x=4, y=8)
    <Coordinate x=96, y=192>

    This will raise a type error if attempting to add something
    other than a Coordinate.

    >>> Coordinate(x=1, y=2) - 5
    Traceback (most recent call last):
    TypeError: Can only subtract Coordinates from Coordinates
"""
