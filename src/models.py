from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
import random
import string

from src.enums import BookStatus
from src.exceptions import BookAlreadyExistsException, BookDoesNotExistException, CollisionException


@dataclass
class Book:
    title: str
    year: int 
    author: str
    status: Enum = BookStatus.IN_STOCK
    id: str | None = None
    
    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "author": self.author,
            "status": self.status.value,
        }

    @classmethod
    def search(cls, fields, storage):
        items = vars(fields).items()
        search_field = None
        search_result = []

        for item in items:
            if item[1]:
                search_field = item
        
        with open(storage, "r") as f:
            lines = f.readlines()
            for line in lines:
                book = json.loads(line)
                if book[search_field[0]] == search_field[1]:
                    search_result.append(book)

    @classmethod
    def print_all(cls, storage):
        with open(storage, "r") as f:  # TODO: просто загрузить файл в память и распечатать? или возможно через try/finally отдать генератор и закрыть файл в finally блоке? 
            books = [json.loads(line) for line in f.readlines()]
        print("||" + "id".center(8, "_") + "||" + "title".center(50, "_") + "||" + "year".center(8, "_") + "||" + "author".center(50, "_") + "||" + "status".center(20, "_") + "||")
        for book in books:
            print("||" + f"{book['id'].center(8)}" + "||" + f"{book['title'].center(50)}" + "||" + f"{str(book['year']).center(8)}" + "||" + f"{book['author'].center(50)}" + "||" + f"{book['status'].center(20)}" + "||")
    
    def delete(self, storage):
        with open(storage, "r+") as f:  # TODO: любое удаление строки из середины файла вызывает необходимость переписывать файл целиком?
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                book = json.loads(line)
                if book["id"] == self.id:
                    continue
                f.write(line)
            f.truncate()

    @classmethod
    def get_by_id(cls, storage, id) -> Book:
        with open(storage, "r") as f:
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
    
    def change_status(self, storage, status):
        with open(storage, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                line = line.rstrip("\n")
                book = json.loads(line)
                if book["id"] == self.id:
                    book["status"] = status
                    f.write(json.dumps(book) + "\n")
                else:
                    f.write(line + "\n")
            f.truncate()

    @classmethod
    def create_object(cls, title, year, author):
        # we use simplistic approach to generating ids just for the sake of time efficency during examination
        id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        book = Book(title=title, year=year, author=author, id=id)
        return book

    def load(self, storage):
        with open(storage, "a+") as f:
            if self._id_exists(f):
                raise CollisionException
            if self._book_exists(f):
                raise BookAlreadyExistsException
            f.write(json.dumps(self.json) + "\n")
    
    def _book_exists(self, file):
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

    def _id_exists(self, file):
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            book = json.loads(line)
            if book["id"] == self.id:
                return True
        return False
