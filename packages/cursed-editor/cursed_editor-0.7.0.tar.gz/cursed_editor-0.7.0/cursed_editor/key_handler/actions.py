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

from .state import State
from ..editor import Editor
from ..coordinate import Coordinate


class BaseAction:
    name = "Unnamed Action"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        raise NotImplementedError


class InsertKey(BaseAction):
    name = "Insert Character at Cursor Position"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.insert(key)
        return state


class MoveUp(BaseAction):
    name = "Move the Cursor Up"
    direction = "up"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        multiplier = max(state.multiplier, 1)
        kwargs = {cls.direction: multiplier}
        editor.move_cursor_relative(**kwargs)
        return State(state, multiplier=0)


class MoveDown(MoveUp):
    name = "Move the Cursor Down"
    direction = "down"


class MoveLeft(MoveUp):
    name = "Move the Cursor Left"
    direction = "left"


class MoveRight(MoveUp):
    name = "Move the Cursor Right"
    direction = "right"


class MoveToLine(BaseAction):
    name = "Move the Cursor to Specific Line"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        y = max(state.multiplier - 1, 0)
        editor.cursor = Coordinate(x=0, y=y)
        return State(state, multiplier=0)


class SwitchToInsertMode(BaseAction):
    name = "Switch to Insert Mode"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        return State(state, mode="insert", multiplier=0)


class SwitchToInsertModeAfter(BaseAction):
    name = "Switch to Insert Mode After Cursor Position"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.move_cursor_relative(right=1)
        return State(state, mode="insert", multiplier=0)


class SwitchToInsertModeAfterLine(BaseAction):
    name = "Switch to Insert Mode At the End of the Cursor Line"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.move_cursor_to_end_of_line()
        return State(state, mode="insert", multiplier=0)


class SwitchToInsertModeStartLine(BaseAction):
    name = "Switch to Insert Mode At the Beginning of the Cursor Line"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.cursor = Coordinate(x=0, y=editor.cursor.y)
        return State(state, mode="insert", multiplier=0)


class SwitchToCommandMode(BaseAction):
    name = "Switch to Command Mode"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        return State(state, mode="command", multiplier=0)


class SwitchToSearchMode(BaseAction):
    name = "Switch to Case Sensitive Search Mode"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        return State(
            state, mode="search", search_string="", case_sensitive_search=True
        )


class SwitchToCaseInsensitiveSearchMode(BaseAction):
    name = "Switch to Case Insensitive Search Mode"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        return State(
            state, mode="search", search_string="", case_sensitive_search=False
        )


class Save(BaseAction):
    name = "Save File"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.save()
        return state


class Delete(BaseAction):
    name = "Deletes Character At Cursor Position"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        multiplier = max(state.multiplier, 1)
        for _ in range(multiplier):
            editor.handle_delete()
        return State(state, multiplier=0)


class DeleteBetween(BaseAction):
    name = "Deletes everything between the two Cursor Locations"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.delete_between()
        return State(state, multiplier=0)


class Backspace(BaseAction):
    name = "Deletes Character Preceeding Cursor Position"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.handle_backspace()
        return state


class StartMultiSelection(BaseAction):
    name = "Sets the secondary cursor position for long selection"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.second_cursor = editor.cursor
        return state


class Copy(BaseAction):
    name = "Copies the Selected Text"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.copy()
        return state


class Paste(BaseAction):
    name = "Copies the Selected Text"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.paste()
        return state


class AddKeyToMultiplier(BaseAction):
    name = "Add Key to Multiplier Number"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        if key in "1234567890":
            multiplier = state.multiplier * 10 + int(key)
            state = State(state, multiplier=multiplier)
        return state


class JoinLines(BaseAction):
    name = "Combine the Current Line with the Following Line"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        multiplier = max(state.multiplier, 1)
        for _ in range(multiplier):
            editor.move_cursor_to_end_of_line()
            editor.handle_delete()
        return State(state, multiplier=0)


class SearchAddCharacter(BaseAction):
    name = "Add Character to Search String"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        state = State(state, search_string=state.search_string + key)
        editor.incremental_search(
            needle=state.search_string,
            mode="same",
            case_sensitive=state.case_sensitive_search,
        )
        return state


class SearchBackspace(BaseAction):
    name = "Remove Last Character from Search String"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        state = State(state, search_string=state.search_string[:-1])
        return state


class FindNext(BaseAction):
    name = "Moves the Cursor to the Next Search Result"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.incremental_search(
            needle=state.search_string,
            case_sensitive=state.case_sensitive_search,
        )
        return state


class FindPrevious(BaseAction):
    name = "Moves the Cursor to the Previous Search Result"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.incremental_search(
            needle=state.search_string,
            mode="reverse",
            case_sensitive=state.case_sensitive_search,
        )
        return state


class Undo(BaseAction):
    name = "Undos the last action"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.undo()
        return state


class Redo(BaseAction):
    name = "Undos the last undone action"

    @classmethod
    def perform(cls, key: str, editor: Editor, state: State) -> State:
        editor.redo()
        return state
