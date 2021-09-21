from library.adapters.repository import AbstractRepository
from library.domain import Book, Review, Author, Publisher
from math import ceil

BOOKS_PER_PAGE = 10


def get_book(repo: AbstractRepository, book_id: int) -> Book:
    return repo.get_book(book_id)


def get_book_reviews(repo: AbstractRepository, book_id: int) -> list[Review]:
    return repo.get_book_reviews(book_id)


def get_author(repo: AbstractRepository, author_id: int) -> Author:
    return repo.get_author(author_id)


def get_filtered_books(repo: AbstractRepository, year: int = None, author_id: int = None, publisher_name: str = None) -> list[Book]:
    books = repo.get_all_books()

    # Filter year
    if year is not None:
        books = [book for book in books if book.release_year == year]

    # Filter author
    if author_id is not None:
        author = repo.get_author(author_id)
        books = [book for book in books if author in book.authors]

    # Filter publisher
    if publisher_name is not None:
        publisher = repo.get_publisher(publisher_name)
        books = [book for book in books if book.publisher == publisher]

    # Sort books alphabetically
    books.sort(key=lambda book: book.title)

    return books


def get_nth_books_page(repo: AbstractRepository, page: int, year: int = None, author_id: int = None, publisher_name: str = None) -> list[Book]:
    books = get_filtered_books(repo, year, author_id, publisher_name)

    return books[page * BOOKS_PER_PAGE - BOOKS_PER_PAGE: page * BOOKS_PER_PAGE]


def get_books_page_count(repo: AbstractRepository, year: int = None, author_id: int = None, publisher_name: str = None) -> int:
    return ceil(len(get_filtered_books(repo, year, author_id, publisher_name)) / BOOKS_PER_PAGE)


def get_all_release_years(repo: AbstractRepository) -> list[int]:
    return repo.get_all_release_years()


def get_all_authors(repo: AbstractRepository) -> list[Author]:
    return sorted(repo.get_all_authors(), key=lambda author: author.full_name)


def get_all_publishers(repo: AbstractRepository) -> list[Publisher]:
    return sorted(repo.get_all_publishers(), key=lambda publisher: publisher.name)


def add_review(repo: AbstractRepository, user_name: str, book_id: int, review_text: str, rating: int):
    book = repo.get_book(book_id)
    review = Review(user_name, book, review_text, rating)
    repo.add_review(review)


def book_to_dict(book: Book) -> {}:
    pass