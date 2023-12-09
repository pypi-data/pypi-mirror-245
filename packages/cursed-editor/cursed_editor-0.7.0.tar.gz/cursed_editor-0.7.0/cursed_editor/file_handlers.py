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

import abc
import os
import logging


logger = logging.getLogger(__name__)


class BaseFileHandler(abc.ABC):
    def __init__(self) -> None:
        self.file_path: str = ""
        self.encoding: str = "utf-8"

    def read(self) -> str:
        raise NotImplementedError

    def save(self, content: str) -> None:
        raise NotImplementedError


class FileHandler(BaseFileHandler):
    def __init__(self) -> None:
        super().__init__()

    def read(self) -> str:
        if not os.path.exists(self.file_path):
            return ""
        with open(self.file_path, "rb") as fref:
            return fref.read().decode(encoding=self.encoding)

    def save(self, content: str) -> None:
        with open(self.file_path, "wb") as fref:
            fref.write(content.encode(encoding=self.encoding))


class NewLineConvertingFileHandler(BaseFileHandler):
    def __init__(self, real_handler: BaseFileHandler, line_ending: str) -> None:
        super().__init__()
        self._real_handler = real_handler
        self._line_ending = line_ending

    def read(self) -> str:
        return self._real_handler.read().replace(self._line_ending, "\n")

    def save(self, content: str) -> None:
        content = content.replace("\n", self._line_ending)
        self._real_handler.save(content)


class MemoryFileHandler(BaseFileHandler):
    def __init__(self) -> None:
        super().__init__()
        self._content = ""

    def read(self) -> str:
        return self._content

    def save(self, content: str) -> None:
        self._content = content
