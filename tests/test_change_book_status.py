from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from books import main
from src.enums import BookStatus
from tests.fixtures.fixtures import test_book, test_book_2, test_book_3, test_change_status_prompt, test_storage_path


class TestChangeBookStatus(unittest.TestCase):
    def setUp(self):
        self.test_books = [test_book.json, test_book_2.json, test_book_3.json]
        with open(test_storage_path, "w+") as f:
            for book in self.test_books:
                f.write(json.dumps(book) + "\n")

    def tearDown(self):
        Path.unlink(test_storage_path, missing_ok=True)

    def test_book_change_status_updates_data_correctly(self):
        test_book.change_status(test_storage_path, BookStatus.OUT_OF_STOCK.value)
        test_book_4 = deepcopy(test_book)
        test_book_4.status = BookStatus.OUT_OF_STOCK
        self.test_books[0] = test_book_4.json
        with open(test_storage_path) as f:
            books = [json.loads(line) for line in f.readlines()]

        self.assertEqual(len(books), len(self.test_books))
        self.assertEqual(books, self.test_books)

    @patch("sys.argv", test_change_status_prompt)
    def test_change_book_status_prints_correct_message(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main(test_storage_path)
        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            f"Book: {test_book.title}, {test_book.year} by {test_book.author}. Status changed to '{test_book.status.value}'\n",
        )
