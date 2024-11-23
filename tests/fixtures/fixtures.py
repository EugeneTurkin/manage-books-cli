from __future__ import annotations

from src.config import config
from src.models import Book


test_storage_path = config.ROOT_PATH / "tests" / "fixtures" / "storage.jsonl"

test_book = Book(title="test title", year=1976, author="test author", id="test")
test_book_2 = Book(title="test title two", year=1977, author="test author", id="TeSt")
test_book_3 = Book(title="different title", year=1976, author="different author", id="TEst")

test_add_prompt = ["book.py", "add", test_book.title, str(test_book.year), test_book.author]
test_del_prompt = ["book.py", "del", test_book.id]
test_change_status_prompt = ["book.py", "status", test_book.id, "out of stock", "-p"]
