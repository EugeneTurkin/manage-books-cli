from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.models import Book
from tests.fixtures.fixtures import test_book, test_book_2, test_book_3, test_storage_path


class TestListBooks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_books = [test_book.json, test_book_2.json, test_book_3.json]
        with open(test_storage_path, "w+") as f:
            for book in cls.test_books:
                f.write(json.dumps(book) + "\n")

    @classmethod
    def tearDownClass(cls):
        Path.unlink(test_storage_path, missing_ok=True)

    def test_book_get_all_returns_correct_data(self):
        books = Book.get_all(test_storage_path)

        self.assertEqual(len(books), len(self.test_books))
        self.assertEqual(books, self.test_books)
