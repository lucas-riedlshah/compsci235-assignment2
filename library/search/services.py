from library.adapters.repository import AbstractRepository
from library.utilities import author_to_dict, book_to_dict, publisher_to_dict


def search_books(repo: AbstractRepository, query: str):
    books = repo.search_books_by_title(query)
    return [book_to_dict(book) for book in books]


def search_authors(repo: AbstractRepository, query: str):
    authors = repo.get_all_authors()
    return [author_to_dict(book) for book in authors]


def search_publishers(repo: AbstractRepository, query: str):
    publishers = repo.get_all_publishers()
    return [publisher_to_dict(book) for book in publishers]
