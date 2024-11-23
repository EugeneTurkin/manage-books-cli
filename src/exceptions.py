from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from src.config import config


if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any


def on_crash(exctype: type[BaseException], value: BaseException, traceback: TracebackType | None) -> Any:
    """Hide traceback for better UE or bring it back for development by changing configuration."""
    if config.SHOW_STACK_TRACE:
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

class StorageFileNotFound(Exception):
    ...
