from pathlib import Path

from src.config import config
from src.models import Book


test_book = Book(title="test title", year=1976, author="test author", id="test")
test_storage_path = config.ROOT_PATH / "tests" / "fixtures" / "storage.jsonl"
test_add_prompt = ["book.py", "add", test_book.title, str(test_book.year), test_book.author]
test_del_prompt = ["book.py", "del", test_book.id]
