from library.adapters.repository import AbstractRepository
from library.domain import Publisher, Book
from math import ceil

PUBLISHERS_PER_PAGE = 25


def get_publisher(repo: AbstractRepository, name: str) -> Publisher:
    return repo.get_publisher(name)


def get_nth_publishers_page(repo: AbstractRepository, page: int) -> list[Publisher]:
    return sorted(repo.get_all_publishers(), key=lambda publisher: publisher.name)[page * PUBLISHERS_PER_PAGE - PUBLISHERS_PER_PAGE: page * PUBLISHERS_PER_PAGE]


def get_publishers_page_count(repo: AbstractRepository) -> int:
    return ceil(len(repo.get_all_publishers()) / PUBLISHERS_PER_PAGE)
