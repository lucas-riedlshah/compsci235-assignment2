import pytest

from library.books.services import *


def test_get_nth_books_page(in_memory_repo):
    assert len(get_nth_books_page(in_memory_repo, 1)) == BOOKS_PER_PAGE


def test_get_books_page_book(in_memory_repo):
    # In the current state of this function, the following assertion will always return true.
    # However, this is fine, as the equation the function is being compared with is without debate, the correct answer.
    # While it might seem this test is useless, it is in fact not, as the get_books_page_count() function could switch
    # a method that uses caching, in which case we would want to compare it with the direct calcution from the repository itself.
    assert get_books_page_count(in_memory_repo) == ceil(
        len(in_memory_repo.get_all_books()) / BOOKS_PER_PAGE)
