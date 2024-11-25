import argparse

from src.enums import BookStatus


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_book_add = subparsers.add_parser("add", help="Add a new book")
    parser_book_add.add_argument("title", type=str, help="Book title. Case insensitive")
    parser_book_add.add_argument("year", type=int, help="Publication year.")
    parser_book_add.add_argument("author", type=str, help="Author's full name. Case insensitive")
    parser_book_add.add_argument("-p", "--print", action="store_true", help="Print out added book's info")

    parser_book_del = subparsers.add_parser("del", help="Delete a book")
    parser_book_del.add_argument("id", type=str, help="Book id")
    parser_book_del.add_argument("-p", "--print", action="store_true", help="Print out deleted book's info")

    parser_book_search = subparsers.add_parser("search", help="Search for a book")
    search_group = parser_book_search.add_mutually_exclusive_group(required=True)
    search_group.add_argument("-t", "--title", type=str, help="Book title. Case insensitive")
    search_group.add_argument("-y", "--year", type=int, help="Publication year.")
    search_group.add_argument("-a", "--author", type=str, help="Author's full name. Case insensitive")

    parser_book_list = subparsers.add_parser("list", help="Print out a list of all the books and their info")

    parser_book_status = subparsers.add_parser("status", help="Delete a book")
    parser_book_status.add_argument("id", type=str, help="Book id")
    parser_book_status.add_argument("status", type=str, help="Book status", choices=BookStatus.values())
    parser_book_status.add_argument("-p", "--print", action="store_true", help="Print out book's info")

    return parser.parse_args()
