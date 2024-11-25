from __future__ import annotations

import json
import random
import string
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from src.enums import BookStatus
from src.exceptions import (
    BookAlreadyExistsException,
    BookDoesNotExistException,
    CollisionException,
    InvalidStatusException,
)


if TYPE_CHECKING:
    from io import TextIOWrapper
    from pathlib import Path
    from typing import Any


@dataclass
class Book:
    title: str
    year: int
    author: str
    status: Enum = BookStatus.IN_STOCK
    id: str | None = None

    @property
    def json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "author": self.author,
            "status": self.status.value,
        }

    @classmethod
    def create_object(cls, title: str, year: int, author: str) -> Book:
        # we use simplistic approach to generating ids just for the sake of time efficency during examination
        id = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        return Book(title=title, year=year, author=author, id=id)

    @classmethod
    def get_all(cls, storage: Path) -> list[dict[str, Any] | None]:
        with storage.open("r") as f:
            books = [json.loads(line) for line in f.readlines()]
        return books

    @classmethod
    def get_by_id(cls, storage: Path, id: str) -> Book:
        with storage.open("r") as f:
            lines = f.readlines()
            for line in lines:
                book = json.loads(line)
                if book["id"] == id:
                    return Book(
                        title=book["title"],
                        year=book["year"],
                        author=book["author"],
                        id=book["id"],
                        status=BookStatus(book["status"]),
                    )
        raise BookDoesNotExistException

    @classmethod
    def search(cls, storage: Path, field: str, value: str | int) -> list[dict[str, Any] | None]:
        results = []
        with storage.open("r") as f:
            for line in f.readlines():
                book = json.loads(line)
                if (
                    value == book[field]
                    or (isinstance(value, str) and value in book[field])
                ):
                    results.append(book)
        return results

    def change_status(self, storage: Path, status: BookStatus) -> None:
        with storage.open("r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                book = json.loads(line)
                if book["id"] != self.id:
                    f.write(line)
                    continue
                if book["status"] == status:
                    raise InvalidStatusException(f"That book's status is already '{status}'") from None
                book["status"] = status
                f.write(json.dumps(book) + "\n")
            f.truncate()

    def delete(self, storage: Path) -> None:
        with storage.open("r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                book = json.loads(line)
                if book["id"] == self.id:
                    continue
                f.write(line)
            f.truncate()

    def load(self, storage: Path) -> None:
        with storage.open("a+") as f:
            if self._id_exists(f):
                raise CollisionException
            if self._book_exists(f):
                raise BookAlreadyExistsException
            f.write(json.dumps(self.json) + "\n")

    def _book_exists(self, file: TextIOWrapper) -> bool:
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            book = json.loads(line)
            if (
                book["author"] == self.author and
                book["title"] == self.title and
                book["year"] == self.year
            ):
                return True
        return False

    def _id_exists(self, file: TextIOWrapper) -> bool:
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            book = json.loads(line)
            if book["id"] == self.id:
                return True
        return False
