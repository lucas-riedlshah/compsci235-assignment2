from datetime import datetime
from .book import Book

class Review:

    def __init__(self, book: Book, review_text: str, rating: int):
        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review_text, str):
            self.__review_text = review_text.strip()
        else:
            self.__review_text = "N/A"

        if isinstance(rating, int) and rating >= 1 and rating <= 5:
            self.__rating = rating
        else:
            raise ValueError

        self.__timestamp = datetime.now()

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return other.book == self.book and other.review_text == self.review_text \
            and other.rating == self.rating and other.timestamp == self.timestamp

    def __repr__(self):
        return f'<Review of book {self.book}, rating = {self.rating}, timestamp = {self.timestamp}>'
