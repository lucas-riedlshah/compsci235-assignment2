from library.adapters.repository import AbstractRepository
from library.domain import Publisher
from math import ceil

PUBLISHERS_PER_PAGE = 25
PUBLISHER_BOOKS_PER_PAGE = 10


def get_publisher(repo: AbstractRepository, name: str) -> Publisher:
    return repo.get_publisher(name)


def get_nth_books_by_publisher_page(repo: AbstractRepository, name: str, page: int) -> list[Book]:
    """Gets the nth books-by-publisher page"""
    books = sorted(repo.get_books_by_publisher(get_publisher(repo, name)),
                   key=lambda book: book.release_year if book.release_year is not None else 99999, reverse=True)
    return books[page * PUBLISHER_BOOKS_PER_PAGE - PUBLISHER_BOOKS_PER_PAGE: page * PUBLISHER_BOOKS_PER_PAGE]


def get_books_by_publisher_page_count(repo: AbstractRepository, name: str) -> int:
    return ceil(len(repo.get_books_by_publisher(get_publisher(repo, name))) / PUBLISHER_BOOKS_PER_PAGE)


def get_nth_publishers_page(repo: AbstractRepository, page: int) -> list[Publisher]:
    return sorted(repo.get_all_publishers(), key=lambda publisher: publisher.name)[page * PUBLISHERS_PER_PAGE - PUBLISHERS_PER_PAGE: page * PUBLISHERS_PER_PAGE]


def get_publishers_page_count(repo: AbstractRepository) -> int:
    return ceil(len(repo.get_all_publishers()) / PUBLISHERS_PER_PAGE)
