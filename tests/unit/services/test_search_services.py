import pytest

from library.search.services import *


def test_search_books(in_memory_repo):
    assert len(search_books(in_memory_repo, 'Superman vol')) == 2
    assert len(search_books(in_memory_repo, '')) == 0


def test_search_authors(in_memory_repo):
    assert len(search_authors(in_memory_repo, 'Jerry Siegel')) == 1
    assert len(search_authors(in_memory_repo, '')) == 0


def test_search_publishers(in_memory_repo):
    assert len(search_publishers(in_memory_repo, 'Avatar pres')) == 1
    assert len(search_publishers(in_memory_repo, '')) == 0
