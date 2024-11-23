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
        book = Book(args.title, args.year, args.author)
        book.add(storage)

        if args.print:
            print(f"Added book: {book.title}, {book.year} by {book.author}")

    if action == Action.DELETE.value:
        Book.delete(args.id)

    if action == Action.SEARCH.value:
        return Book.search(args)

    if action == Action.LIST.value:
        Book.print_all()

    if action == Action.STATUS.value:
        Book.change_status(args)

    return vars(args)


if __name__ == "__main__":
    main()
