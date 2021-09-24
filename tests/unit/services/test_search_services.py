import pytest

from library.search.services import *


def test_search_books(in_memory_repo):
    assert len(search_books(in_memory_repo, "")) == 0
    assert len(search_books(in_memory_repo, "  .  ")) == 0
    assert len(search_books(in_memory_repo, "vol")) == 10
    assert len(search_books(in_memory_repo, "superman vol. 1")) == 3


def test_search_authors(in_memory_repo):
    assert len(search_authors(in_memory_repo, "")) == 0
    assert len(search_authors(in_memory_repo, "  .  ")) == 0
    assert len(search_authors(in_memory_repo, "Takashi murakami")) == 1
    assert len(search_authors(in_memory_repo, "a.")) == 23


def test_search_publishers(in_memory_repo):
    assert len(search_publishers(in_memory_repo, "")) == 0
    assert len(search_publishers(in_memory_repo, "  .  ")) == 0
    assert len(search_publishers(in_memory_repo, "a")) == 9
    assert len(search_publishers(in_memory_repo, "DC Marvel")) == 2
