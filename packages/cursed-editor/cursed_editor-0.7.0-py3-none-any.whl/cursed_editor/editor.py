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

from .window import Window
from .file_handlers import BaseFileHandler, NewLineConvertingFileHandler
from .configuration import Config
from .coordinate import Coordinate
from .tabbed_editor import TabbedEditor


logger = logging.getLogger(__name__)


class Editor:
    def __init__(
        self,
        file_handler: BaseFileHandler,
        config: Config = Config(),
    ) -> None:
        self._config = config
        self._file_handler = NewLineConvertingFileHandler(
            real_handler=file_handler,
            line_ending=config.line_ending,
        )
        self._tabbed_editor = TabbedEditor(
            content=self._file_handler.read(),
            tab_width=config.tab_display_width,
        )

    @property
    def cursor(self) -> Coordinate:
        return self._tabbed_editor.cursor

    @cursor.setter
    def cursor(self, value: Coordinate) -> None:
        self._tabbed_editor.cursor = value

    @property
    def second_cursor(self) -> Coordinate:
        return self._tabbed_editor.second_cursor

    @second_cursor.setter
    def second_cursor(self, value: Coordinate) -> None:
        self._tabbed_editor.second_cursor = value

    def handle_delete(self, length: int = 1) -> None:
        self._tabbed_editor.handle_delete(length)

    def delete_between(self) -> None:
        self._tabbed_editor.delete_between()

    def copy(self) -> None:
        self._tabbed_editor.copy()

    def paste(self) -> None:
        self._tabbed_editor.paste()

    def undo(self) -> None:
        self._tabbed_editor.undo()

    def redo(self) -> None:
        self._tabbed_editor.redo()

    def handle_backspace(self) -> None:
        if self._config.expand_tabs:
            length = 1
            start_x = self.cursor.x - 1
            mod = start_x % self._config.expand_tabs
            if mod == 0:
                mod = self._config.expand_tabs - 1
            start_x = max(start_x - mod, 0)
            line = self._tabbed_editor.expanded_lines[self.cursor.y]
            text = set(line[start_x : self.cursor.x])
            if text == set(" "):
                length = mod + 1
            self.move_cursor_relative(left=length)
            self.handle_delete(length=length)
        else:
            self._tabbed_editor.handle_backspace()

    def insert(self, character_to_add: str) -> None:
        if character_to_add == "\t" and self._config.expand_tabs:
            mod = (
                self._config.expand_tabs - self.cursor.x
            ) % self._config.expand_tabs
            if not mod:
                mod = self._config.expand_tabs
            character_to_add = " " * mod
        self._tabbed_editor.insert(character_to_add)

    def move_cursor_relative(
        self,
        *,
        up: int = 0,
        down: int = 0,
        left: int = 0,
        right: int = 0,
    ) -> None:
        self._tabbed_editor.move_cursor_relative(
            up=up,
            down=down,
            left=left,
            right=right,
        )

    def move_cursor_to_end_of_line(self) -> None:
        line = self._tabbed_editor.expanded_lines[self.cursor.y]
        self.cursor = Coordinate(x=len(line), y=self.cursor.y)

    def get_lines_for_window(self, window: Window) -> List[str]:
        top = window.top
        bottom = window.bottom
        lines = self._tabbed_editor.expanded_lines[top : bottom + 1]
        final_lines = []
        for line in lines:
            line_segment = line[window.left : window.right]
            final_lines.append(line_segment)
        return final_lines

    def incremental_search(
        self,
        needle: str,
        mode: str = "normal",
        case_sensitive: bool = True,
    ) -> None:
        self._tabbed_editor.incremental_search(
            needle=needle, mode=mode, case_sensitive=case_sensitive
        )

    def __str__(self) -> str:
        return str(self._tabbed_editor)

    def save(self) -> None:
        self._file_handler.save(str(self))
