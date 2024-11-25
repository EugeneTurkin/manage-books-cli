from __future__ import annotations

import sys
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Final


SHOW_STACK_TRACE: Final = False

def on_crash(exctype: Exception, value: str, traceback: str) -> None:
    if SHOW_STACK_TRACE:
        sys.__excepthook__(exctype, value, traceback)
    else:
        print(exctype.__name__ + ":", value)

sys.excepthook = on_crash


class InvalidStatusException(Exception):
    ...


class BookAlreadyExistsException(Exception):
    ...


class BookDoesNotExistException(Exception):
    ...


class CollisionException(Exception):
    ...
