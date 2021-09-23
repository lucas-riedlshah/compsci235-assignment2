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

    def search_books_by_title(self, query: str) -> list[Book]:
        # remove any non-word or whitespace characters using regex. (aka remove punctuation)
        query = re.sub(r'[^\w\s]', '', query).strip().lower()
        if len(query) == 0:
            return []
        query_words = query.split(" ")
        books = []
        distances = []  # A list of integers describing how similar the book's title is to the search query
        for book in self.__books.values():
            distance = len(query_words)
            title = book.title.lower()
            if len(query_words) == 1:
                distance -= title.count(query_words[0])
            else:
                for word in query_words:
                    if word in title.split(" "):
                        distance -= title.count(word)
            if distance != len(query_words):
                books.append(book)
                distances.append(distance)
        # Sort books by distance
        books = [book for _, book in sorted(zip(distances, books))]
        return books

    def search_authors_by_full_name(self, query: str) -> list[Author]:
        # remove any non-word or whitespace characters using regex. (aka remove punctuation)
        query = re.sub(r'[^\w\s]', '', query).strip().lower()
        if len(query) == 0:
            return []
        query_words = query.split(" ")
        authors = []
        distances = []  # A list of integers describing how similar the author's title is to the search query
        for author in self.__authors.values():
            distance = len(query_words)
            full_name = author.full_name.lower()
            if len(query_words) == 1:
                distance -= full_name.count(query_words[0])
            else:
                for word in query_words:
                    if word in full_name.split(" "):
                        distance -= full_name.count(word)
            if distance != len(query_words):
                authors.append(author)
                distances.append(distance)
        # Sort authors by distance
        authors = [author for _, author in sorted(zip(distances, authors))]
        return authors

    def search_publishers_by_name(self, query: str) -> list[Publisher]:
        # remove any non-word or whitespace characters using regex. (aka remove punctuation)
        query = re.sub(r'[^\w\s]', '', query).strip().lower()
        if len(query) == 0:
            return []
        query_words = query.split(" ")
        publishers = []
        distances = []  # A list of integers describing how similar the publisher's title is to the search query
        for publisher in self.__publishers.values():
            distance = len(query_words)
            name = publisher.name.lower()
            if len(query_words) == 1:
                distance -= name.count(query_words[0])
            else:
                for word in query_words:
                    if word in name.split(" "):
                        distance -= name.count(word)
            if distance != len(query_words):
                publishers.append(publisher)
                distances.append(distance)
        # Sort publishers by distance
        publishers = [publisher for _, publisher in sorted(
            zip(distances, publishers))]
        return publishers

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
