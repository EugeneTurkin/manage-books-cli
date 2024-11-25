from __future__ import annotations

import json
from pathlib import Path
import unittest

from tests.fixtures.fixtures import test_book, test_book_2, test_book_3, test_storage_path
from src.models import Book


class TestSearchBooks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_books = [test_book.json, test_book_2.json, test_book_3.json]
        with open(test_storage_path, "w+") as f:
            for book in cls.test_books:
                f.write(json.dumps(book) + "\n")

    @classmethod
    def tearDownClass(cls):
        Path.unlink(test_storage_path, missing_ok=True)
    
    def test_book_search_by_title_returns_correct_output(self):
        books = Book.search(test_storage_path, "title", "test title")

        self.assertEqual(len(books), 2)
        self.assertEqual(books, self.test_books[:2])

    def test_book_search_by_author_returns_correct_output(self):
        books = Book.search(test_storage_path, "author", "test author")

        self.assertEqual(len(books), 2)
        self.assertEqual(books, self.test_books[:2])

    def test_book_search_by_year_returns_correct_output(self):
        books = Book.search(test_storage_path, "year", 1976)

        self.assertEqual(len(books), 2)
        self.assertEqual(books, self.test_books[::2])

    def test_book_search_returns_empty_list_when_not_found(self):
        books = Book.search(test_storage_path, "year", 2000)

        self.assertEqual(len(books), 0)
