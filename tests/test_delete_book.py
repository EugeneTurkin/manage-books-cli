from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from books import main
from src.exceptions import BookDoesNotExistException
from src.models import Book
from tests.fixtures.fixtures import test_book, test_del_prompt, test_storage_path


class TestDeleteBook(unittest.TestCase):
    def setUp(self):
        with open(test_storage_path, "w+") as f:
            f.write(json.dumps(test_book.json) + "\n")

    def tearDown(self):
        Path.unlink(test_storage_path, missing_ok=True)

    def test_book_get_by_id_returns_correct_data(self):
        book = Book.get_by_id(test_storage_path, test_book.id)

        self.assertEqual(book.title, test_book.title)
        self.assertEqual(book.year, test_book.year)
        self.assertEqual(book.author, test_book.author)
        self.assertEqual(book.status, test_book.status)

    def test_book_delete_deletes_data_correctly(self):
        test_book.delete(test_storage_path)
        with open(test_storage_path) as f:
            lines = f.readlines()

        self.assertEqual(lines, [])

    @patch("sys.argv", test_del_prompt + ["-p"])
    def test_del_book_prints_correct_message(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main(test_storage_path)
        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            f"Deleted book: {test_book.title}, {test_book.year} by {test_book.author}\n",
        )


class TestDeleteBookExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_book_json = test_book.json
        test_book_json["id"] = "TeSt"
        with open(test_storage_path, "w+") as f:
            f.write(json.dumps(test_book_json) + "\n")

    @classmethod
    def tearDownClass(cls):
        Path.unlink(test_storage_path, missing_ok=True)

    def test_book_get_by_id_raises_does_not_exist(self):
        with self.assertRaises(BookDoesNotExistException):
            Book.get_by_id(test_storage_path, test_book.id)
