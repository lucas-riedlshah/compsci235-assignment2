import pytest

from library.domain import Review, User
from library.books.services import *


def test_get_book(in_memory_repo):
    assert get_book(in_memory_repo, 25742454).title == "The Switchblade Mamma"


def test_get_book_reviews(in_memory_repo):
    book = get_book(in_memory_repo, 25742454)
    assert len(get_book_reviews(in_memory_repo, book.book_id)) == 0

    user = User("lucas", "ABC123xyz")
    in_memory_repo.add_user(user)
    review = Review("lucas", book, "review text content", 3)
    in_memory_repo.add_review(review)
    assert len(get_book_reviews(in_memory_repo, book.book_id)) == 1


def test_get_author(in_memory_repo):
    assert get_author(in_memory_repo, 81563).full_name == "Jerry Siegel"


def test_get_filtered_books(in_memory_repo):
    assert len(get_filtered_books(
        in_memory_repo, 1997, 81563, "DC Comics")) == 1
    assert len(get_filtered_books(
        in_memory_repo, 1997, 5, "Marvel")) == 0


def test_get_nth_books_page(in_memory_repo):
    assert len(get_nth_books_page(in_memory_repo, 1)) == BOOKS_PER_PAGE
    assert len(get_nth_books_page(in_memory_repo, 1, 2016)) == 5
    assert len(get_nth_books_page(in_memory_repo, 1, 2016, 14965)) == 2
    assert len(get_nth_books_page(in_memory_repo,
               1, 2016, 14965, "Avatar Press")) == 2


def test_get_books_page_count(in_memory_repo):
    assert get_books_page_count(in_memory_repo) == 2
    assert get_books_page_count(in_memory_repo, 2012) == 1
    assert get_books_page_count(
        in_memory_repo, 2012, 14965, "Avatar Press") == 0


def test_get_all_release_years(in_memory_repo):
    assert len(get_all_release_years(in_memory_repo)) == 8


def test_get_all_authors(in_memory_repo):
    assert len(get_all_authors(in_memory_repo)) == 31


def test_get_all_publishers(in_memory_repo):
    assert len(get_all_publishers(in_memory_repo)) == 11


def test_add_review(in_memory_repo):
    user = User("lucas", "ABC123xyz")
    in_memory_repo.add_user(user)
    add_review(in_memory_repo, "lucas", 25742454, "review text content", 3)
    assert get_book_reviews(in_memory_repo, 25742454)[
        0].review_text == "review text content"
