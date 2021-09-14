import abc
from typing import List
from datetime import date

from library.domain.model import Publisher, Author, Book, Review, User

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a `Book` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        """ Returns the `Book` with the given `book_id` from the repository.

            If no such `Book` exist, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self) -> List[Book]:
        """ Returns a list of all `Book`s in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_book(self, book_id: int):
        """ Removes a `Book` from the repository. """
    def search_books_by_title(self, title: str) -> List[Book]:
        """ Returns a list of `Book`s who's title(s) contain the given string

            If no such `Book`s exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_books_by_author_name(self, author_name: str) -> List[Book]:
        """ Returns a list of `Book`s who's `Author`(s) name(s) contain the given string

            If no such `Book`s exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_books_by_release_year(self, release_year: int) -> List[Book]:
        """ Returns a list of `Book`s who's `release_year` contains the given value.

            If no such `Book`s exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_books_by_publisher_name(self, publisher_name: str) -> List[Book]:
        """ Returns a list of `Book`s who's `Publisher` name contains the given string

            If no such `Book`s exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author) -> List[Book]:
        """ Returns a list of `Book`s by the given `Author`

            If no such `Author` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_from_release_year(self, release_year: int) -> List[Book]:
        """ Returns a list of `Book`s released in the given `release_year`.
            Unlike `search_books_by_release_year()`, this will only return exact matches.

            If no `Book`s from the given year exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        """ Returns a list of `Book`s from the given `Publisher`

            If no such `Publisher` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a `User` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the `User` named `user_name` from the repository.

            If there is no `User` with the given `user_name`, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a `Review` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_reviews(self, book: Book) -> List[Review]:
        """ Returns a list of `Review`s of the given `Book`.

            If no reviews exist, returns an empty list.
        """
        raise NotImplementedError
