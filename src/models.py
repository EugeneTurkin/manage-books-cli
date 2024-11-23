from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
import random
import string

from src.enums import BookStatus
from src.exceptions import BookAlreadyExistsException, CollisionException


@dataclass
class Book:
    title: str
    year: int 
    author: str
    status: Enum = BookStatus.IN_STOCK
    id: str | None = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
    
    @property
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "author": self.author,
            "status": self.status.value,
        }

    @classmethod
    def print_all(cls, storage):
        with open(storage, "r") as f:  # TODO: просто загрузить файл в память и распечатать? или возможно через try/finally отдать генератор и закрыть файл в finally блоке? 
            lines = f.readline()
            print(lines)

    @classmethod
    def delete(cls, id, storage):
        with open(storage, "r+") as f:  # TODO: любое удаление строки из середины файла вызывает необходимость переписывать файл целиком?
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                line1 = json.loads(line)
                if line1["id"] == id:
                    continue
                f.write(line)
            f.truncate()

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
        
        return search_result
    
    @classmethod
    def change_status(cls, args, storage):
        with open(storage, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                line = line.rstrip("\n")
                book = json.loads(line)
                if book["id"] == args.id:
                    book["status"] = args.status
                    f.write(json.dumps(book) + "\n")
                else:
                    f.write(line + "\n")
            f.truncate()

    def add(self, storage):
        if self._exists(storage):
            raise BookAlreadyExistsException

        with open(storage, "a+") as f:
            f.write(json.dumps(self.to_json) + "\n")
    
    def _exists(self, storage):
        with open(storage, "a+") as f:
            f.seek(0)
            lines = f.readlines()
            for line in lines:
                book = json.loads(line)
                if book["id"] == self.id:
                    raise CollisionException
                if (
                    book["author"] == self.author and
                    book["title"] == self.title and
                    book["year"] == self.year
                ):
                    return True
            return False
