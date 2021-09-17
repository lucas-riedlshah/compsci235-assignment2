from library.adapters.repository import AbstractRepository
from library.domain import Author
from math import ceil

AUTHORS_PER_PAGE = 25
AUTHOR_BOOKS_PER_PAGE = 10

def get_author(repo: AbstractRepository, author_id: int):
    return repo.get_author(author_id)

def get_nth_books_by_author_page(repo: AbstractRepository, author_id: int, page: int):
    books = sorted(repo.get_books_by_author(get_author(repo, author_id)), key=lambda book: book.release_year, reverse=True)
    return books[page * AUTHOR_BOOKS_PER_PAGE - AUTHOR_BOOKS_PER_PAGE: page * AUTHOR_BOOKS_PER_PAGE]

def get_books_by_author_page_count(repo: AbstractRepository, author_id: int):
    return ceil(len(repo.get_books_by_author(get_author(repo, author_id))) / AUTHOR_BOOKS_PER_PAGE)

def get_nth_authors_page(repo: AbstractRepository, page: int) -> list[Author]:
    return sorted(repo.get_all_authors(), key=lambda author: author.full_name)[page * AUTHORS_PER_PAGE - AUTHORS_PER_PAGE: page * AUTHORS_PER_PAGE]

def get_authors_page_count(repo: AbstractRepository):
    return ceil(len(repo.get_all_authors()) / AUTHORS_PER_PAGE)