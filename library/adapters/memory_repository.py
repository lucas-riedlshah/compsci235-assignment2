from bisect import insort_left

from library.adapters.repository import AbstractRepository
from library.domain import Book, User, Author, Publisher, Review


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__books = {}
        self.__authors = {}
        self.__publishers = {}
        self.__users = {}
        self.__reviews = {}

    def add_book(self, book: Book):
        self.__books[book.book_id] = book

    def get_book(self, book_id: int) -> Book:
        if book_id in self.__books:
            return self.__books[book_id]

    def get_all_books(self) -> list[Book]:
        return list(self.__books.values())

    def add_publisher(self, publisher: Publisher):
        self.__publishers[publisher.name] = publisher

    def get_publisher(self, name: str) -> Publisher:
        if name in self.__publishers:
            return self.__publishers[name]

    def get_all_publishers(self) -> list[Publisher]:
        return list(self.__publishers.values())

    def add_author(self, author: Author):
        self.__authors[author.unique_id] = author

    def get_author(self, unique_id: int) -> Author:
        if unique_id in self.__authors:
            return self.__authors[unique_id]

    def get_all_authors(self) -> list[Author]:
        return list(self.__authors.values())

    def get_all_release_years(self) -> list[int]:
        release_years = []
        for book in self.__books.values():
            if book.release_year is not None and book.release_year not in release_years:
                insort_left(release_years, book.release_year)
        return release_years

    def search_books_by_title(self, title: str) -> list[Book]:
        results = []
        title = title.strip()
        if title == "":
            return results
        for book in self.__books.values():
            if title in book.title.lower():
                results.append(book)
        return results

    def search_books_by_author_name(self, author_name: str) -> list[Book]:
        results = []
        author_name = author_name.strip()
        if author_name == "":
            return results
        for book in self.__books.values():
            for author in book.authors:
                if author_name in author.full_name.lower():
                    results.append(book)
        return results

    def search_books_by_release_year(self, release_year: str) -> list[Book]:
        results = []
        release_year = release_year.strip()
        if release_year == "":
            return results
        for book in self.__books.values():
            if release_year in str(book.release_year):
                results.append(book)
        return results

    def search_books_by_publisher_name(self, publisher_name: str) -> list[Book]:
        results = []
        publisher_name = publisher_name.strip()
        if publisher_name == "":
            return results
        for book in self.__books.values():
            if publisher_name in book.publisher.name.lower():
                results.append(book)
        return results

    def get_books_by_author(self, author: Author) -> list[Book]:
        if author.unique_id not in self.__authors:
            return None
        results = []
        for book in self.__books.values():
            if author in book.authors:
                results.append(book)
        return results

    def get_books_from_release_year(self, release_year: int) -> list[Book]:
        results = []
        for book in self.__books.values():
            if release_year == book.release_year:
                results.append(book)
        return results

    def get_books_by_publisher(self, publisher: Publisher) -> list[Book]:
        if publisher.name not in self.__publishers:
            return None
        results = []
        for book in self.__books.values():
            if publisher == book.publisher:
                results.append(book)
        return results

    def add_user(self, user: User):
        self.__users[user.user_name] = user

    def get_user(self, user_name) -> User:
        if user_name in self.__users:
            return self.__users[user_name]

    def add_review(self, review: Review):
        if review.book.book_id not in self.__reviews:
            self.__reviews[review.book.book_id] = []
        self.__reviews[review.book.book_id].append(review)

    def get_book_reviews(self, book: Book) -> list[Review]:
        if book.book_id in self.__reviews:
            return self.__reviews[book.book_id]
        return []