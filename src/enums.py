from __future__ import annotations

from enum import Enum


class Base(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [value.value for value in cls.__members__.values()]


class Action(Base):
    ADD = "add"
    DELETE = "del"
    SEARCH = "search"
    LIST = "list"
    STATUS = "status"


class BookStatus(Base):
    IN_STOCK = "in stock"
    OUT_OF_STOCK = "out of stock"
