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

from typing import List, Union


class BaseTrigger:
    def __init__(self, name: str) -> None:
        self.name = name

    def is_triggered(self, key: str) -> bool:
        raise NotImplementedError


class SimpleTrigger(BaseTrigger):
    def __init__(self, key: str) -> None:
        super().__init__(f'The "{key}" Key')
        self.__key = key

    def is_triggered(self, key: str) -> bool:
        return key == self.__key


class KeysTrigger(BaseTrigger):
    def __init__(
        self, name: str, keys: Union[int, str, List[Union[int, str]]]
    ) -> None:
        super().__init__(name)
        self.__keys = []
        if isinstance(keys, (int, str)):
            keys = [keys]
        for key in keys:
            if isinstance(key, int):
                key = chr(key)
            self.__keys.append(key)

    def is_triggered(self, key: str) -> bool:
        return key in self.__keys


class AnyOtherKeyTrigger(BaseTrigger):
    def __init__(self) -> None:
        super().__init__("Any Other Key")

    def is_triggered(self, key: str) -> bool:
        return len(key) == 1


control_s = KeysTrigger("Control+s", 19)
escape = KeysTrigger("Escape", 27)
delete = KeysTrigger("Delete", "KEY_DC")
enter = KeysTrigger("Enter ", "\n")
backspace = KeysTrigger("Backspace", ["KEY_BACKSPACE", 127])

numeric = KeysTrigger("Any Digit", list("1234567890"))

key_up = KeysTrigger("Up Arrow Key", "KEY_UP")
key_down = KeysTrigger("Down Arrow Key", "KEY_DOWN")
key_left = KeysTrigger("Left Arrow Key", "KEY_LEFT")
key_right = KeysTrigger("Right Arrow Key", "KEY_RIGHT")

any_other = AnyOtherKeyTrigger()
