from library.adapters.repository import AbstractRepository
from library.utilities import book_to_dict

def get_recommended_books(repo: AbstractRepository, book_ids: list[int]):
    books = []
    for id in book_ids:
        books.append(book_to_dict(repo.get_book(id)))
    return books