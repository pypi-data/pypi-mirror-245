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
import sys
import curses
import time
import argparse
import logging
import logging.config

from typing import Optional, IO, AnyStr, List, Union

from .editor import Editor
from .window import Window
from .key_handler.handler import KeyHandler
from .file_handlers import BaseFileHandler, FileHandler
from .configuration import ConfigManager, Config

VERSION = "unknown"

logger = logging.getLogger(__name__)


def setup_logging(config: Config) -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {},
            "filters": {},
            "handlers": {
                "file_handler": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "filename": config.log_file,
                    "mode": "w",
                },
            },
            "disable_existing_loggers": False,
            "loggers": {},
            "root": {
                "level": config.log_level,
                "handlers": ["file_handler"],
            },
        }
    )
    logger.info("logging initiated")


class Application:
    def __init__(self, file_handler: BaseFileHandler, config: Config) -> None:
        self._config = config
        self._editor = Editor(
            file_handler,
            config=config,
        )
        self._key_handler = KeyHandler(self._editor)
        self._window = Window(width=50, height=50)

    def main(self) -> None:
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(self._wrapped_curses_app)

    def _wrapped_curses_app(self, stdscr: curses.window) -> None:
        try:
            curses.nl()
            self._initialize_screen(stdscr)
            curses.use_default_colors()
            self._mainloop(stdscr)
        except KeyboardInterrupt:
            logger.info("got keyboard interrupt. Closing application")
        except Exception as err:  # pragma: no cover pylint: disable=broad-except
            logger.exception(err)

    def _initialize_screen(self, stdscr: curses.window) -> None:
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.nodelay(True)
        self._set_size(stdscr)
        self._redraw_from_editor(stdscr)

    def _set_size(self, stdscr: curses.window) -> None:
        self._window.height, self._window.width = stdscr.getmaxyx()

    def _mainloop(self, stdscr: curses.window) -> None:
        logger.info("mainloop started")
        while True:
            self._check_resize(stdscr)
            self._check_keypress(stdscr)
            time.sleep(0.01)

    def _check_resize(self, stdscr: curses.window) -> None:
        if curses.is_term_resized(self._window.height, self._window.width):
            logger.info("New Screen Size: %s", stdscr.getmaxyx())
            self._set_size(stdscr)
            self._redraw_from_editor(stdscr)

    def _check_keypress(self, stdscr: curses.window) -> None:
        key = self._get_key(stdscr)
        if key is not None:
            self._handle_key(stdscr, key)

    def _get_key(self, stdscr: curses.window) -> Optional[str]:
        key: Union[int, str, None] = None
        try:
            key = stdscr.get_wch()
        except curses.error:
            pass
        if isinstance(key, int):
            key = curses.keyname(key).decode()
        return key

    def _handle_key(self, stdscr: curses.window, key: str) -> None:
        logger.info('Typed Character: key="%s" ordinal=%s', key, ord(key[:1]))
        logger.info("length=%s", len(key))
        if key == "KEY_RESIZE":
            self._check_resize(stdscr)
        else:
            self._key_handler.handle_key(key)
            self._redraw_from_editor(stdscr)

    def _redraw_from_editor(self, stdscr: curses.window) -> None:
        stdscr.clear()
        self._move_cursor(stdscr, x=0, y=0)
        self._window.cursor = self._editor.cursor
        lines = self._editor.get_lines_for_window(self._window)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self._draw_character(stdscr, char, x, y)
        self._move_cursor(
            stdscr,
            x=self._window.cursor.x,
            y=self._window.cursor.y,
        )

    def _draw_character(
        self, stdscr: curses.window, character: str, x: int, y: int
    ) -> None:
        try:
            stdscr.addch(y, x, character[:1])
        except curses.error:
            pass

    def _move_cursor(self, stdscr: curses.window, *, x: int, y: int) -> None:
        x = min(self._window.width - 1, max(0, x))
        y = min(self._window.height - 1, max(0, y))
        stdscr.move(y, x)


def _setup_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cursed",
        description="A Vim inspired Text Editor Written in Pure Python",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--config_file",
        help="The path to the user's config file",
        default=os.path.expanduser("~/.cursed.conf"),
    )
    parser.add_argument(
        "-e",
        "--encoding",
        help="The encoding to use to read and write the file",
        default=sys.getdefaultencoding(),
    )

    group_ex = parser.add_mutually_exclusive_group()

    group_ex.add_argument(
        "--keymap", help="Show the Key Bindings", action="store_true"
    )
    group_ex.add_argument(
        "--print-config",
        help="Print the current configuration",
        action="store_true",
    )
    group_ex.add_argument(
        "--version", help="Print the Program Version", action="store_true"
    )
    group_ex.add_argument(
        "filename", help="The file to edit", nargs="?", default=""
    )
    return parser


def main(
    *,
    args: Optional[List[str]] = None,
    stdout: Optional[IO[AnyStr]] = None,
    file_handler: Optional[BaseFileHandler] = None,
) -> None:
    parser = _setup_argument_parser()
    parsed = parser.parse_args(args)
    manager = ConfigManager()
    manager.read(parsed.config_file)
    manager.read_project_configuration(parsed.filename)
    config = manager.get_effective_configuration()
    setup_logging(config)
    if file_handler is None:
        file_handler = FileHandler()
        file_handler.encoding = parsed.encoding
    if parsed.filename != "":
        file_handler.file_path = parsed.filename
        app = Application(file_handler, config=config)
        app.main()
    elif parsed.version:
        print(VERSION, file=stdout)
    elif parsed.keymap:
        print(KeyHandler.help_text(), file=stdout)
    elif parsed.print_config:
        print(manager.write_config_to_string(), file=stdout)
    else:
        print(parser.format_help(), file=stdout)


if __name__ == "__main__":
    main()
VERSION = "0.7.0"
