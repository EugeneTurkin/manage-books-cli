class AlreadyInStockException(Exception):
    ...


class AlreadyOutOfStockException(Exception):
    ...


class BookAlreadyExistsException(Exception):
    ...


class BookDoesNotExistException(Exception):
    ...


class CollisionException(Exception):
    ...
