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
        """Make jsonable dict out of object's attributes."""
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
        return Book(title=title.lower(), year=year, author=author.lower(), id=id)

    @classmethod
    def get_all(cls, storage: Path) -> list[dict[str, Any]]:
        with storage.open("r") as f:
            books = [json.loads(line) for line in f.readlines()]
        return books

    @classmethod
    def get_by_id(cls, storage: Path, id: str) -> Book:
        """Iterate through storage and return matching object, throw exception otherwise."""
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
        msg = "No book matches provided data"
        raise BookDoesNotExistException(msg)

    @classmethod
    def search(cls, storage: Path, field: str, value: str | int) -> list[dict[str, Any]]:
        """Iterate through storage and return matching dicts, or an empty list if no book matches provided field."""
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
        """Rewrite storage file, updating the instance.

        If provided status matches current status, throw an exception.
        """
        with storage.open("r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                book = json.loads(line)
                if book["id"] != self.id:
                    f.write(line)
                    continue
                if book["status"] == status:
                    msg = f"That book's status is already '{status}'"
                    raise InvalidStatusException(msg)
                book["status"] = status
                f.write(json.dumps(book) + "\n")
            f.truncate()

    def delete(self, storage: Path) -> None:
        """Rewrite storage file omitting the instance, effectively deleting it's data from storage."""
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
        """Load object to storage file if it's id and data are unique, otherwise throw respective exceptions."""
        with storage.open("a+") as f:
            if self._id_exists(f):
                msg = "During generating book's id a collision has occured. Just try again."
                raise CollisionException(msg)
            if self._book_exists(f):
                msg = "Provided data matches a book that is already loaded to storage"
                raise BookAlreadyExistsException(msg)
            f.write(json.dumps(self.json) + "\n")

    def _book_exists(self, file: TextIOWrapper) -> bool:
        """Return true if there is a line in storage containing provided data, False otherwise."""
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
        """Return true if there is a line in storage containing provided id, False otherwise."""
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            book = json.loads(line)
            if book["id"] == self.id:
                return True
        return False
