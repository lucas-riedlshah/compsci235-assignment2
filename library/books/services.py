from library.adapters.repository import AbstractRepository
from library.domain import Book
from math import ceil

BOOKS_PER_PAGE = 10

def get_book(repo: AbstractRepository):
    pass

def get_nth_books_page(repo: AbstractRepository, page: int) -> list[Book]:
    return repo.get_all_books()[page * BOOKS_PER_PAGE - BOOKS_PER_PAGE: page * BOOKS_PER_PAGE]

def get_books_page_count(repo: AbstractRepository):
    return ceil(len(repo.get_all_books()) / BOOKS_PER_PAGE)