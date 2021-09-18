import pytest

from library.authors.services import *


def test_get_author(in_memory_repo):
    assert get_author(
        in_memory_repo, 6869276).full_name == "Takashi   Murakami"


def test_get_nth_books_by_author_page(in_memory_repo):
    assert len(get_nth_books_by_author_page(in_memory_repo, 14965, 1)) == 2


def test_get_books_by_author_page_count(in_memory_repo):
    assert get_books_by_author_page_count(in_memory_repo, 14965) == 1


def test_get_nth_authors_page(in_memory_repo):
    assert len(get_nth_authors_page(in_memory_repo, 1)) == 25
    assert len(get_nth_authors_page(in_memory_repo, 2)) == 6


def test_get_authors_page_count(in_memory_repo):
    assert get_authors_page_count(in_memory_repo) == 2
