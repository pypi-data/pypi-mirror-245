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

from enum import Enum
from typing import Optional, List, Union, Tuple

logger = logging.getLogger(__name__)


class EventType(Enum):
    FIRST = "first"
    INSERTION = "insertion"
    DELETION = "deletion"


class Event:
    def __init__(
        self,
        event_type: EventType,
        *,
        position: int = 0,
        text: str = "",
    ) -> None:
        self.next: Optional[Event] = None
        self.previous: Optional[Event] = None
        self.text = text
        self.position = position
        self.event_type = event_type

    def __repr__(self) -> str:
        has_next = self.next is not None
        has_previous = self.previous is not None
        event_type = self.event_type
        text = self.text
        position = self.position
        return (
            f"<Event {event_type=} {text=} {position=} "
            f"{has_next=} {has_previous=}>"
        )


class MutableString:
    def __init__(self, content: str) -> None:
        self._content = content
        self._last_event = Event(EventType.FIRST)

    def __repr__(self) -> str:
        return f"<MutableString content={repr(self._content)}>"

    def __str__(self) -> str:
        return self._content

    def to_string(self) -> str:
        return str(self)

    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> str:
        if isinstance(index, tuple):
            return self._content[index[0] : index[1] + 1]
        if index < 0 or index >= len(self._content):
            return ""
        return self._content[index]

    def insert(self, *, text: str, index: int) -> "MutableString":
        return self._insert(text=text, index=index, add_event=True)

    def _insert(
        self, *, text: str, index: int, add_event: bool
    ) -> "MutableString":
        if not text:
            return self
        index = max(index, 0)
        if index <= len(self._content):
            before = self._content[:index]
            after = self._content[index:]
            self._content = before + text + after
        else:
            index = len(self._content)
            self._content = self._content + text
        if add_event:
            new_event = Event(EventType.INSERTION, position=index, text=text)
            self._add_event(new_event)
        return self

    def _add_event(self, new_event: Event) -> None:
        logger.info(f"adding event {new_event}")
        self._last_event.next = new_event
        new_event.previous = self._last_event
        self._last_event = new_event

    def undo(self) -> Optional[int]:
        event = self._last_event
        result = None
        if event.event_type == EventType.INSERTION:
            self._delete(
                add_event=False, start=event.position, length=len(event.text)
            )
            result = event.position
        elif event.event_type == EventType.DELETION:
            self._insert(add_event=False, index=event.position, text=event.text)
            result = event.position + len(event.text)
        if event.previous is not None:
            self._last_event = event.previous
        return result

    def redo(self) -> Optional[int]:
        event = self._last_event
        result = None
        if event.next is not None:
            self._last_event = event.next
            event = self._last_event
            if event.event_type == EventType.INSERTION:
                self._insert(
                    add_event=False, index=event.position, text=event.text
                )
                result = event.position + len(event.text)
            else:
                self._delete(
                    add_event=False,
                    start=event.position,
                    length=len(event.text),
                )
                result = event.position
        return result

    def delete(
        self,
        *,
        start: int = 0,
        end: Optional[int] = None,
        length: Optional[int] = None,
    ) -> "MutableString":
        return self._delete(start=start, end=end, length=length, add_event=True)

    def _delete(
        self,
        *,
        add_event: bool,
        start: int = 0,
        end: Optional[int] = None,
        length: Optional[int] = None,
    ) -> "MutableString":
        if length is not None and end is not None:
            raise ValueError(
                "cannot pass values for both end and length parameters"
            )
        if end is not None:
            end = min(end, len(self._content) - 1)
        elif length is None:
            end = len(self._content) - 1
        elif length <= 0:
            return self
        else:
            end = start + length - 1
        start = max(start, 0)
        if start >= len(self._content):
            return self
        if end < start:
            return self
        end = end + 1
        before = self._content[:start]
        middle = self._content[start:end]
        after = self._content[end:]
        if add_event:
            new_event = Event(EventType.DELETION, position=start, text=middle)
            self._add_event(new_event)
        self._content = before + after
        return self

    def search(self, *, needle: str, case_sensitive: bool = True) -> List[int]:
        result: List[int] = []
        if not needle:
            return result
        content = self._content
        if not case_sensitive:
            content = content.lower()
            needle = needle.lower()
        current = content.find(needle)
        while current != -1:
            result.append(current)
            current = self._content.find(needle, current + 1)
        return result


MutableString.__init__.__doc__ = """
    Initializes a MutableString object.
    >>> MutableString("the rain in spain")
    <MutableString content='the rain in spain'>
"""

MutableString.__str__.__doc__ = """
    Returns the contents of the MutableString as a str
    >>> str(MutableString("a b c d e f g"))
    'a b c d e f g'
"""

MutableString.to_string.__doc__ = """
    Equivalent to str(self).  Helpful for method chaining.
    >>> MutableString("a b c d e f g").to_string()
    'a b c d e f g'
"""


MutableString.delete.__doc__ = """
    Deletes the text between the given indices (inclusively).

    >>> MutableString("I am funny and smart").delete(start=8, end=9)
    <MutableString content='I am fun and smart'>

    >>> MutableString("I am funny, and smart").delete(start=10, end=10)
    <MutableString content='I am funny and smart'>

    >>> MutableString("").delete(start=8, end=9)
    <MutableString content=''>

    Instead of providing the end parameter, passing a length is also
    acceptable.

    >>> MutableString("I am funny and smart").delete(start=8, length=2)
    <MutableString content='I am fun and smart'>

    >>> MutableString("I am funny, and smart").delete(start=10, length=1)
    <MutableString content='I am funny and smart'>

    Passing length<=0 results in no change to the string

    >>> MutableString("I am funny and smart").delete(start=5, length=0)
    <MutableString content='I am funny and smart'>

    >>> MutableString("I am funny and smart").delete(start=5, length=-1)
    <MutableString content='I am funny and smart'>

    Passing start by itself removes all trailing text from the string.

    >>> MutableString("I am funny, and smart").delete(start=8)
    <MutableString content='I am fun'>

    Any starting index less than zero is assumed to be zero.

    >>> MutableString("I am funny, and smart").delete(start=-15, end=11)
    <MutableString content='and smart'>

    Note that the ending index is capped to the end of the string.

    >>> MutableString("I am funny, and smart").delete(start=10, end=1900)
    <MutableString content='I am funny'>

    >>> MutableString("I am funny, and smart").delete(start=-11, end=1900)
    <MutableString content=''>

    However, The start parameter is optional and defaults to 0 (zero).

    >>> MutableString("I am funny and smart").delete(end=14)
    <MutableString content='smart'>

    Passing length by itself also works.

    >>> MutableString("I am funny and smart").delete(length=15)
    <MutableString content='smart'>

    By now you may have noticed that end = start + length - 1.
    This is because I wanted "end" to be inclusive, which is
    contrary to how slicing normally works in python.

    As a result, passing length=0 results in no change to the string

    >>> MutableString("I am funny and smart").delete(start=5, length=0)
    <MutableString content='I am funny and smart'>

    To truncate the entire string, simply call delete without any arguments.

    >>> MutableString("I am funny and smart").delete()
    <MutableString content=''>

    If the end is less than the start, nothing is deleted:

    >>> MutableString("I am funny and smart").delete(start=5, end=3)
    <MutableString content='I am funny and smart'>

    The end and length parameters cannot both be specified simultaneously

    >>> MutableString("I am funny and smart").delete(start=5, end=7, length=4)
    Traceback (most recent call last):
    ValueError: cannot pass values for both end and length parameters


    Tired of hearing how funny and smart I am?   So is my wife hahaha.
"""

MutableString.search.__doc__ = r"""
    Search the text for the string contained in the needle parameter.

    Returns a list containing the the starting positions where the string
    is found.

    >>> haystack = "the rain\nin west\tspain\nmainly\ndrains in the plain."
    >>> mut = MutableString(haystack)

    >>> mut.search(needle="ain")
    [5, 19, 24, 32, 46]

    >>> mut.search(needle="goober")
    []

"""
