import pytest

from library.books.services import *


def test_get_book(in_memory_repo):
    assert get_book(in_memory_repo, 25742454).title == "The Switchblade Mamma"


def test_get_nth_books_page(in_memory_repo):
    assert len(get_nth_books_page(in_memory_repo, 1)) == BOOKS_PER_PAGE
    assert len(get_nth_books_page(in_memory_repo, 1, 2016)) == 5


def test_get_books_page_count(in_memory_repo):
    assert get_books_page_count(in_memory_repo) == 2
    assert get_books_page_count(in_memory_repo, 2012) == 1


def test_get_all_release_years(in_memory_repo):
    assert len(get_all_release_years(in_memory_repo)) == 8
