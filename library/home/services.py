from library.adapters.repository import AbstractRepository
from library.utilities import book_to_dict

def get_recent_books(repo: AbstractRepository):
    books = sorted(repo.get_all_books(), key=lambda book: book.release_year or 0, reverse=True)[:4]
    return books