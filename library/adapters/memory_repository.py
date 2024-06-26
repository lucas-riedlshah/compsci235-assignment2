import re
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
        user = self.get_user(review.user_name)
        for i in range(len(user.reviews)):
            if user.reviews[i].book == review.book:
                repository_book_review_index = self.__reviews[review.book.book_id].index(
                    user.reviews[i])
                self.__reviews[review.book.book_id].pop(
                    repository_book_review_index)
                user.reviews.pop(i)
                break
        insort_left(user.reviews, review)
        insort_left(self.__reviews[review.book.book_id], review)

    def get_book_reviews(self, book_id: int) -> list[Review]:
        if book_id in self.__reviews:
            return self.__reviews[book_id]
        return []
