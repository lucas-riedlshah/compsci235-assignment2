import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain import Author, Book, Publisher, Review, User

def test_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(0, 'Parry Hotter')
    repo.add_book(book)

    assert repo.get_book(0) is book

def test_get_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert isinstance(repo.get_book(11827783), Book)

def test_get_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert repo.get_book(42) is None

def test_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert isinstance(repo.get_all_books(), list)
    assert len(repo.get_all_books()) > 0

def test_get_books_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = repo.get_all_authors()[0]
    assert len(repo.get_books_by_author(author)) == 1

def test_get_books_by_non_existent_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = Author(666, "Lucifer")
    assert repo.get_books_by_author(author) is None

def test_get_books_from_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_books_from_release_year(2)) == 0
    assert len(repo.get_books_from_release_year(2012)) == 13

def test_get_all_release_years(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_all_release_years()) == 20

def test_get_books_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = repo.get_all_publishers()[0]
    assert len(repo.get_books_by_publisher(publisher)) == 1

def test_get_books_by_non_existent_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher("Lucas RiedlShah Publications Inc.")
    assert repo.get_books_by_publisher(publisher) is None

def test_add_user_and_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('dave', '123456789')
    repo.add_user(user)

    assert repo.get_user('dave') is user

def test_get_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_add_review_get_book_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(0, 'Star Trek: The Next Generation')
    user = User("lucas", "ABC123xyz")
    repo.add_user(user)
    review = Review(user.user_name, book, "Resistance is futile.", 5)
    repo.add_review(review)
    assert len(repo.get_book_reviews(book.book_id)) == 1