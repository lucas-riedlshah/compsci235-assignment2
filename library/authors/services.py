from math import ceil

from library.adapters.repository import AbstractRepository
from library.domain import Author, Book
from library.utilities import author_to_dict

AUTHORS_PER_PAGE = 25


def get_nth_authors_page(repo: AbstractRepository, page: int):
    authors = sorted(repo.get_all_authors(), key=lambda author: author.full_name)[
        page * AUTHORS_PER_PAGE - AUTHORS_PER_PAGE: page * AUTHORS_PER_PAGE]
    return [author_to_dict(author) for author in authors]


def get_authors_page_count(repo: AbstractRepository):
    return ceil(len(repo.get_all_authors()) / AUTHORS_PER_PAGE)
