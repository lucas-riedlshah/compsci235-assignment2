from math import ceil

from library.adapters.repository import AbstractRepository
from library.domain import Publisher, Book
from library.utilities import publisher_to_dict

PUBLISHERS_PER_PAGE = 25


def get_nth_publishers_page(repo: AbstractRepository, page: int) -> list[Publisher]:
    publishers = sorted(repo.get_all_publishers(), key=lambda publisher: publisher.name)[page * PUBLISHERS_PER_PAGE - PUBLISHERS_PER_PAGE: page * PUBLISHERS_PER_PAGE]
    return [publisher_to_dict(publisher) for publisher in publishers]

def get_publishers_page_count(repo: AbstractRepository) -> int:
    return ceil(len(repo.get_all_publishers()) / PUBLISHERS_PER_PAGE)
