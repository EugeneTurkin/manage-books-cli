"""Controller module for manage-books app."""

from pathlib import Path
import sys

from src.cli import parse_args
from src.config import config
from src.enums import Action
from src.exceptions import StorageFileNotFound
from src.models import Book
from src.utils import table_print


def main(
    storage: Path = config.DATA_PATH,
) -> None:
    action = sys.argv[1]
    args = parse_args()

    if action == Action.ADD.value:
        book = Book.create_object(args.title, args.year, args.author)
        book.load(storage)

        if args.print:
            print(f"Added book: {book.title}, {book.year} by {book.author}")

    if action == Action.DELETE.value:
        book = Book.get_by_id(storage, args.id)
        book.delete(storage)

        if args.print:
            print(f"Deleted book: {book.title}, {book.year} by {book.author}")

    if action == Action.SEARCH.value:
        items = vars(args).items()
        for item in items:
            if item[1]:
                field, value = item
        if books := Book.search(storage, field, value):
            table_print(books)
        else:
            print("No books found")

    if action == Action.LIST.value:
        books = Book.get_all(storage)
        table_print(books)

    if action == Action.STATUS.value:
        book = Book.get_by_id(storage, args.id)
        book.change_status(storage, args.status)

        if args.print:
            print(f"Book: {book.title}, {book.year} by {book.author}. Status changed to '{book.status.value}'")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        msg = "Storage file not yet created. Try adding a book or creating storage manually."
        raise StorageFileNotFound(msg)
