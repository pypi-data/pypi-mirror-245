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

import logging

from typing import List

from .lined_editor import LinedEditor
from .coordinate import Coordinate
from .utils import string_to_lines

logger = logging.getLogger(__name__)


class TabbedEditor:
    def __init__(
        self,
        content: str = "",
        tab_width: int = 4,
    ) -> None:
        self._lined_editor = LinedEditor(content=content)
        self._tab_width = tab_width

    def __str__(self) -> str:
        return str(self._lined_editor)

    @property
    def cursor(self) -> Coordinate:
        return self._untabbed_to_tabbed(self._lined_editor.cursor)

    @cursor.setter
    def cursor(self, value: Coordinate) -> None:
        self._lined_editor.cursor = self._tabbed_to_untabbed(value)

    @property
    def second_cursor(self) -> Coordinate:
        return self._untabbed_to_tabbed(self._lined_editor.second_cursor)

    @second_cursor.setter
    def second_cursor(self, value: Coordinate) -> None:
        self._lined_editor.second_cursor = self._tabbed_to_untabbed(value)

    @property
    def expanded_lines(self) -> List[str]:
        text = str(self).replace("\t", "\t" * self._tab_width)
        return string_to_lines(text)

    def _tabbed_to_untabbed(self, coordinate: Coordinate) -> Coordinate:
        lines = string_to_lines(str(self._lined_editor))
        y = max(coordinate.y, 0)
        y = min(y, len(lines) - 1)
        line = lines[y]
        line = line.replace("\t", "\t" * self._tab_width)
        x = max(coordinate.x, 0)
        line = line[:x]
        splitup = line.split("\t" * self._tab_width)
        last = splitup.pop().rstrip("\t")
        splitup.append(last)
        line = "\t".join(splitup)
        x = len(line)
        return Coordinate(y=y, x=x)

    def _untabbed_to_tabbed(self, coordinate: Coordinate) -> Coordinate:
        lines = string_to_lines(str(self._lined_editor))
        y = max(coordinate.y, 0)
        y = min(y, len(lines) - 1)
        line = lines[y]
        x = max(coordinate.x, 0)
        line = line[:x]
        line = line.replace("\t", "\t" * self._tab_width)
        x = len(line)
        return Coordinate(x=x, y=y)

    def move_cursor_relative(
        self,
        *,
        up: int = 0,
        down: int = 0,
        left: int = 0,
        right: int = 0,
    ) -> None:
        y = self._lined_editor.cursor.y
        y = y + down - up
        x = self._lined_editor.cursor.x
        x = x + right - left
        self._lined_editor.cursor = Coordinate(x=x, y=y)

    def handle_delete(self, length: int = 1) -> None:
        self._lined_editor.handle_delete(length=length)

    def delete_between(self) -> None:
        self._lined_editor.delete_between()

    def copy(self) -> None:
        self._lined_editor.copy()

    def paste(self) -> None:
        self._lined_editor.paste()

    def undo(self) -> None:
        self._lined_editor.undo()

    def redo(self) -> None:
        self._lined_editor.redo()

    def handle_backspace(self) -> None:
        self._lined_editor.handle_backspace()

    def insert(self, character_to_add: str) -> None:
        self._lined_editor.insert(character_to_add)

    def incremental_search(
        self,
        needle: str,
        mode: str = "normal",
        case_sensitive: bool = True,
    ) -> None:
        self._lined_editor.incremental_search(
            needle=needle, mode=mode, case_sensitive=case_sensitive
        )
