from pathlib import Path
import sys

from src.cli import parse_args
from src.config import config
from src.enums import Action
from src.models import Book


def main(
    storage: Path = config.DATA_PATH,  # TODO: норм или нет?
):
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
        # return Book.search(args)
        print([vars(args)])

    if action == Action.LIST.value:
        Book.print_all(storage)

    if action == Action.STATUS.value:
        book = Book.get_by_id(storage, args.id)
        book.change_status(storage, args.status)

        if args.print:
            print(f"Book: {book.title}, {book.year} by {book.author}. Status changed to {book.status}")


if __name__ == "__main__":
    main()
