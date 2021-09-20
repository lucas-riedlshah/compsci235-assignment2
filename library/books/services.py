from library.adapters.repository import AbstractRepository
from library.domain import Book, Review
from math import ceil

BOOKS_PER_PAGE = 10

def get_book(repo: AbstractRepository, book_id: int) -> Book:
    return repo.get_book(book_id)

def get_book_reviews(repo: AbstractRepository, book: Book) -> list[Review]:
    return repo.get_book_reviews(book)

def get_nth_books_page(repo: AbstractRepository, page: int, year: int = None) -> list[Book]:
    if year is None:
        return repo.get_all_books()[page * BOOKS_PER_PAGE - BOOKS_PER_PAGE: page * BOOKS_PER_PAGE]
    else:
        return repo.get_books_from_release_year(year)[page * BOOKS_PER_PAGE - BOOKS_PER_PAGE: page * BOOKS_PER_PAGE]

def get_books_page_count(repo: AbstractRepository, year: int = None) -> int:
    if year is None:
        return ceil(len(repo.get_all_books()) / BOOKS_PER_PAGE)
    else:
        return ceil(len(repo.get_books_from_release_year(year)) / BOOKS_PER_PAGE)

def get_all_release_years(repo: AbstractRepository) -> list[int]:
    return repo.get_all_release_years()
