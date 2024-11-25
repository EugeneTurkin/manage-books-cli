from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from books import main 
from src.exceptions import BookAlreadyExistsException, CollisionException
from src.models import Book
from tests.fixtures.fixtures import test_book, test_add_prompt, test_storage_path


class TestAddBook(unittest.TestCase):
    def tearDown(self):
        Path.unlink(test_storage_path, missing_ok=True)
    
    def test_create_object_creates_object_correctly(self):
        book = Book.create_object(test_book.title, test_book.year, test_book.author)

        self.assertIsInstance(book.id, str)
        self.assertEqual(len(book.id), 4)
        self.assertTrue(re.fullmatch(r"[A-Za-z0-9]*", book.id))
        self.assertEqual(book.title, test_book.title)
        self.assertEqual(book.year, test_book.year)
        self.assertEqual(book.author, test_book.author)
        self.assertEqual(book.status, test_book.status)

    def test_book_load_loads_data_correctly(self):
        test_book.load(test_storage_path)
        with open(test_storage_path, "r") as f:
            book = f.readline()
            book = json.loads(book)

        self.assertEqual(book["id"], test_book.id)
        self.assertEqual(book["title"], test_book.title)
        self.assertEqual(book["year"], test_book.year)
        self.assertEqual(book["author"], test_book.author)
        self.assertEqual(book["status"], test_book.status.value)

    @patch("sys.argv", test_add_prompt + ["-p"])
    def test_add_book_prints_correct_message(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main(test_storage_path)
        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            f"Added book: {test_book.title}, {test_book.year} by {test_book.author}\n"
        )


class TestBookLoadExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        json_test_book = {
            "id": test_book.id,
            "title": test_book.title,
            "year": test_book.year,
            "author": test_book.author,
            "status": test_book.status.value,
        }
        with open(test_storage_path, "w+") as f:
            f.write(json.dumps(json_test_book) + "\n")

    @classmethod
    def tearDownClass(cls):
        Path.unlink(test_storage_path, missing_ok=True)

    def test_book_load_raises_collision_exc(self):
        with self.assertRaises(CollisionException):
            test_book.load(test_storage_path)
    
    @patch("sys.argv", test_add_prompt)
    def test_book_load_raises_book_already_exists_exc(self):
        with self.assertRaises(BookAlreadyExistsException):
            test_book_2 = deepcopy(test_book)
            test_book_2.id = "TeSt"
            test_book_2.load(test_storage_path)
