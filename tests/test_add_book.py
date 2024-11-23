from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from books import main 
from src.config import config
from src.exceptions import BookAlreadyExistsException, CollisionException
from src.models import Book


test_book = Book(title="test title", year=1976, author="test author", id="test")
test_storage_path = Path(__file__).parent / "fixtures" / "storage.jsonl"
test_book_prompt = ["book.py", "add", test_book.title, str(test_book.year), test_book.author]


class TestAddBook(unittest.TestCase):
    def tearDown(self):
        Path.unlink(test_storage_path, missing_ok=True)

    @patch("sys.argv", test_book_prompt)
    def test_storage_file_created(self):
        main(test_storage_path)
        self.assertTrue(test_storage_path.exists())

    @patch("sys.argv", test_book_prompt)
    def test_add_book_loads_data_correctly(self):
        main(test_storage_path)
        with open(test_storage_path, "r") as f:
            book = f.readline()
            book = json.loads(book)
        self.assertEqual(book["title"], test_book.title)
        self.assertEqual(book["year"], test_book.year)
        self.assertEqual(book["author"], test_book.author)
        self.assertEqual(book["status"], test_book.status.value)

    @patch("sys.argv", test_book_prompt + ["-p"])
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


class TestAddBookExceptions(unittest.TestCase):
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

    def test_add_book_raises_collision_exc(self):
        with self.assertRaises(CollisionException):
            test_book.add(test_storage_path)
    
    @patch("sys.argv", test_book_prompt)
    def test_add_book_raises_book_already_exists_exc(self):
        with self.assertRaises(BookAlreadyExistsException):
            main(test_storage_path)
