import abc
from datetime import date

from tqdm import tqdm

from .jsondatareader import BooksJSONReader
from library.domain import Publisher, Author, Book, Review, User

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a `Book` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        """ Returns the `Book` with the given `book_id` from the repository.

            If no such `Book` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self) -> list[Book]:
        """ Returns a list of all `Book`s in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        """ Adds a `Publisher` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self, name: str) -> Publisher:
        """ Returns the `Publisher` with the given `name` from the repository.

            If no such `Publisher` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_publishers(self) -> list[Publisher]:
        """ Returns a list of all `Publisher`s. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Adds a `Author` to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, unique_id: int) -> Author:
        """ Returns the `Author` with the given `unique_id` from the repository.

            If no such `Author` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_authors(self) -> list[Author]:
        """ Returns a list of all `Author`s. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_release_years(self) -> list[int]:
        """ Returns a list of all release years """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author) -> list[Book]:
        """ Returns a list of `Book`s by the given `Author`

            If no such `Author` exists, returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_from_release_year(self, release_year: int) -> list[Book]:
        """ Returns a list of `Book`s released in the given `release_year`.

            If no `Book`s from the given year exist, returns empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher(self, publisher: Publisher) -> list[Book]:
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
    def get_book_reviews(self, book_id: int) -> list[Review]:
        """ Returns a list of `Review`s of the given `Book`.

            If no reviews exist, returns an empty list.
        """
        raise NotImplementedError


repo_instance: AbstractRepository = None


def populate(path: str, repository: AbstractRepository, database_mode=False):
    print("POPULATING...")
    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'
    path_to_books_file = str(path / books_file_name)
    path_to_authors_file = str(path / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)

    reader.read_json_files()

    for book in tqdm(reader.dataset_of_books):
        repository.add_book(book)
        if not database_mode:
            if book.publisher.name != "N/A":
                repository.add_publisher(book.publisher)
            for author in book.authors:
                repository.add_author(author)
    print("FINSIHED POPULATING.")
