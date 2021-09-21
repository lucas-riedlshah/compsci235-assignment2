from library.adapters.repository import AbstractRepository
from library.domain import Author, Book
from math import ceil

AUTHORS_PER_PAGE = 25


def get_author(repo: AbstractRepository, author_id: int):
    return repo.get_author(author_id)


def get_nth_authors_page(repo: AbstractRepository, page: int) -> list[Author]:
    return sorted(repo.get_all_authors(), key=lambda author: author.full_name)[page * AUTHORS_PER_PAGE - AUTHORS_PER_PAGE: page * AUTHORS_PER_PAGE]


def get_authors_page_count(repo: AbstractRepository):
    return ceil(len(repo.get_all_authors()) / AUTHORS_PER_PAGE)
