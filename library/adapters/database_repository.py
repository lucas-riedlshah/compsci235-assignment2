from datetime import date
from bisect import insort_left

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain import Book, User, Author, Publisher, Review
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(
            self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(
            self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, book_id: int) -> Book:
        try:
            return self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            return None

    def get_all_books(self) -> list[Book]:
        return self._session_cm.session.query(Book).all()

    def add_publisher(self, publisher: Publisher):
        if self.get_publisher(publisher.name) is None:
            with self._session_cm as scm:
                scm.session.add(publisher)
                scm.commit()

    def get_publisher(self, name: str) -> Publisher:
        try:
            return self._session_cm.session.query(Publisher).filter(Publisher._Publisher__name == name).one()
        except NoResultFound:
            return None

    def get_all_publishers(self) -> list[Publisher]:
        # Exclude N/A
        return self._session_cm.session.query(Publisher).filter(Publisher._Publisher__name != 'N/A').all()

    def add_author(self, author: Author):
        if self.get_author(author.unique_id) is None:
            with self._session_cm as scm:
                scm.session.add(author)
                scm.commit()

    def get_author(self, unique_id: int) -> Author:
        try:
            return self._session_cm.session.query(Author).filter(Author._Author__unique_id == unique_id).one()
        except NoResultFound:
            return None

    def get_all_authors(self) -> list[Author]:
        return self._session_cm.session.query(Author).all()

    def get_all_release_years(self) -> list[int]:
        release_years = []
        for book in self.get_all_books():
            if book.release_year is not None and book.release_year not in release_years:
                insort_left(release_years, book.release_year)
        return release_years

    def get_books_by_author(self, author: Author) -> list[Book]:
        if author.unique_id not in [author.unique_id for author in self.get_all_authors()]:
            return None
        results = []
        for book in self.get_all_books():
            if author in book.authors:
                results.append(book)
        return results

    def get_books_from_release_year(self, release_year: int) -> list[Book]:
        results = []
        for book in self.get_all_books():
            if release_year == book.release_year:
                results.append(book)
        return results

    def get_books_by_publisher(self, publisher: Publisher) -> list[Book]:
        if publisher not in self.get_all_publishers():
            return None
        results = []
        for book in self.get_all_books():
            if publisher == book.publisher:
                results.append(book)
        return results

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        try:
            return self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            return None

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.query(Review).filter(Review._Review__user_name == review.user_name).delete()
            scm.session.add(review)
            scm.commit()

    def get_book_reviews(self, book_id: int) -> list[Review]:
        try:
            return self._session_cm.session.query(Review).filter(Review._Review__book == self.get_book(book_id)).all()
        except NoResultFound:
            return None
