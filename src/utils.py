"""Utilities for src package."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any


def table_print(books: list[dict[str, Any]]) -> None:
    """Print books in an improvized table representation."""
    print(
        "||" + "id".center(8, "_") +
        "||" + "title".center(50, "_") +
        "||" + "year".center(8, "_") +
        "||" + "author".center(50, "_") +
        "||" + "status".center(20, "_") + "||",
    )
    for book in books:
        print(
            "||" + f"{book['id'].center(8)}" +
            "||" + f"{book['title'].center(50)}" +
            "||" + f"{str(book['year']).center(8)}" +
            "||" + f"{book['author'].center(50)}" +
            "||" + f"{book['status'].center(20)}" + "||")
