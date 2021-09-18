import pytest

from library.publishers.services import *


def test_get_publisher(in_memory_repo):
    assert get_publisher(in_memory_repo, "Marvel").name == "Marvel"


def test_get_nth_books_by_publisher_page(in_memory_repo):
    assert len(get_nth_books_by_publisher_page(
        in_memory_repo, "DC Comics", 1)) == 1


def test_get_books_by_publisher_page_count(in_memory_repo):
    assert get_books_by_publisher_page_count(in_memory_repo, "Avatar Press") == 1


def test_get_nth_publishers_page(in_memory_repo):
    assert len(get_nth_publishers_page(in_memory_repo, 1)) == 11


def test_get_publishers_page_count(in_memory_repo):
    assert get_publishers_page_count(in_memory_repo) == 1
