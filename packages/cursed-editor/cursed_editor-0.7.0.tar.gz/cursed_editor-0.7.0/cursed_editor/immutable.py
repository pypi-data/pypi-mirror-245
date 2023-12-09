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

from typing import Optional


def is_public(some_attribute: str) -> bool:
    return not some_attribute.startswith("_")


class Immutable:
    def __init__(
        self, state: Optional["Immutable"] = None, **kwargs: object
    ) -> None:
        args = {}
        if state is not None:
            args.update(state.__dict__)
        args.update(kwargs)
        for key in filter(is_public, self.__class__.__dict__.keys()):
            default = self.__class__.__dict__[key]
        for key, default in self.__class__.__dict__.items():
            self.__setattr__(key, args.get(key, default))
        self._is_setup = True

    def __setattr__(self, key: str, value: object) -> None:
        if hasattr(self, "_is_setup"):
            raise TypeError("can't modify state")
        super().__setattr__(key, value)
