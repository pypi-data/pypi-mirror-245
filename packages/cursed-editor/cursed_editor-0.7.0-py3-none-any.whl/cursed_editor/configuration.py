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

import os
import io
import configparser
import logging

from pathlib import Path

from typing import List, Optional, Union, Mapping, Any

from .immutable import Immutable


class Config(Immutable):
    tab_display_width = 4
    expand_tabs = 0
    log_file = "~/.cursed.log"
    log_level = logging.WARNING
    line_ending = "\n"


class ConfigManager:
    def __init__(self) -> None:
        self._parser = configparser.ConfigParser(default_section="default")
        default_configuration: Mapping[str, Mapping[str, Any]] = {
            "default": {
                "tab_display_width": 4,
                "expand_tabs": 0,
                "log_file": "~/.cursed.log",
                "log_level": logging.WARNING,
                "line_ending": r"\n",
            },
            "extension:py": {"expand_tabs": 4},
        }
        self._parser.read_dict(default_configuration)
        self._path_of_file_to_edit: str = ""

    def read_project_configuration(self, path_of_file_to_edit: str) -> None:
        self._path_of_file_to_edit = path_of_file_to_edit
        paths = self._get_project_configuration(path_of_file_to_edit)
        self.read(paths)

    def read(
        self, filepath: Union[str, List[Path]], encoding: Optional[str] = None
    ) -> None:
        self._parser.read(filepath, encoding=encoding)

    def _get_project_configuration(
        self, path_of_file_to_edit: str
    ) -> List[Path]:
        result = []
        if path_of_file_to_edit == "":
            cwd = Path(os.getcwd())
            parents = [cwd] + list(cwd.parents)
        else:
            parents = list(Path(path_of_file_to_edit).parents)
        for folder in parents:
            testpath = folder.joinpath(".cursed.conf")
            if os.path.exists(testpath):
                result.append(testpath)
                break
        return result

    def write_config_to_string(self) -> str:
        fref = io.StringIO()
        self._parser.write(fref)
        fref.seek(0)
        return fref.read()

    def _get_section(self) -> configparser.SectionProxy:
        if self._path_of_file_to_edit == "":
            return self._parser["default"]
        path = Path(self._path_of_file_to_edit)
        section = "extension:" + "".join(path.suffixes)[1:]
        if self._parser.has_section(section):
            return self._parser[section]
        section = "extension:" + path.suffix[1:]
        if self._parser.has_section(section):
            return self._parser[section]
        return self._parser["default"]

    def get_effective_configuration(self) -> Config:
        section = self._get_section()
        path = section["log_file"]
        path = os.path.abspath(os.path.expanduser(path))

        line_ending = section["line_ending"]
        line_ending = line_ending.replace(r"\r", "\r")
        line_ending = line_ending.replace(r"\n", "\n")

        return Config(
            tab_display_width=section.getint("tab_display_width"),
            expand_tabs=section.getint("expand_tabs"),
            log_file=path,
            log_level=section.getint("log_level"),
            line_ending=line_ending,
        )
