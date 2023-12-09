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

from .linear_editor import LinearEditor
from .coordinate import Coordinate
from .utils import string_to_lines


logger = logging.getLogger(__name__)


class LinedEditor:
    def __init__(
        self,
        content: str = "",
    ) -> None:
        self._linear_editor = LinearEditor(content)

    def __str__(self) -> str:
        return str(self._linear_editor)

    def _bound_coordinate(self, coordinate: Coordinate) -> Coordinate:
        lines = str(self._linear_editor).split("\n")
        y = max(coordinate.y, 0)
        y = min(y, len(lines) - 1)
        x = max(coordinate.x, 0)
        x = min(x, len(lines[y]))
        # not subtracting one from len(lines[y]) allows for
        # "sitting on the line ending" or being "at the end of the line"
        return Coordinate(x=x, y=y)

    @property
    def cursor(self) -> Coordinate:
        return self._coordinate_for_index(self._linear_editor.cursor)

    @cursor.setter
    def cursor(self, value: Coordinate) -> None:
        self._linear_editor.cursor = self._index_for_coordinate(value)

    @property
    def second_cursor(self) -> Coordinate:
        return self._coordinate_for_index(self._linear_editor.second_cursor)

    @second_cursor.setter
    def second_cursor(self, value: Coordinate) -> None:
        self._linear_editor.second_cursor = self._index_for_coordinate(value)

    def _index_for_coordinate(self, coordinate: Coordinate) -> int:
        coordinate = self._bound_coordinate(coordinate)
        text = str(self._linear_editor)
        lines = string_to_lines(text)
        prior_lines = lines[: coordinate.y]
        current_line = lines[coordinate.y]
        current_line = current_line[: coordinate.x]
        prior_lines.append(current_line)
        prior_string = "".join(prior_lines)
        return len(prior_string)

    def _coordinate_for_index(self, index: int) -> Coordinate:
        text = str(self._linear_editor)[:index]
        lines = text.split("\n")
        last_line = lines.pop()
        y = len(lines)
        x = len(last_line)
        return Coordinate(y=y, x=x)

    def handle_delete(self, length: int = 1) -> None:
        self._linear_editor.handle_delete(length=length)

    def delete_between(self) -> None:
        self._linear_editor.delete_between()

    def handle_backspace(self) -> None:
        self._linear_editor.handle_backspace()

    def insert(self, character_to_add: str) -> None:
        self._linear_editor.insert(character_to_add)

    def copy(self) -> None:
        self._linear_editor.copy()

    def paste(self) -> None:
        self._linear_editor.paste()

    def undo(self) -> None:
        self._linear_editor.undo()

    def redo(self) -> None:
        self._linear_editor.redo()

    def incremental_search(
        self,
        needle: str,
        mode: str = "normal",
        case_sensitive: bool = True,
    ) -> None:
        self._linear_editor.incremental_search(
            needle=needle, mode=mode, case_sensitive=case_sensitive
        )
