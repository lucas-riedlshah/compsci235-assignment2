from pathlib import Path
import pytest

from utils import get_project_root

from library.domain import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader


class TestBooksJSONReader:

    def test_read_books_from_file(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert str(
            dataset_of_books[0]) == "<Book The Switchblade Mamma, book id = 25742454>"
        assert str(
            dataset_of_books[9]) == "<Book War Stories, Volume 4, book id = 27036539>"
        assert str(
            dataset_of_books[19]) == "<Book D.Gray-man, Vol. 16: Blood & Chains, book id = 18955715>"

    def test_read_books_from_file_and_check_authors(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert str(dataset_of_books[0].authors[0]
                   ) == "<Author Lindsey Schussman, author id = 8551671>"
        assert str(dataset_of_books[15].authors[0]
                   ) == "<Author Maki Minami, author id = 791996>"
        assert len(dataset_of_books[3].authors) == 2
        assert str(dataset_of_books[3].authors[1]
                   ) == "<Author Chris  Martin, author id = 853385>"

    def test_read_books_from_file_and_check_other_attributes(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert dataset_of_books[2].release_year == 2012
        assert dataset_of_books[19].description == "Lenalee is determined to confront a Level 4 Akuma that's out to kill Komui, but her only chance is to reclaim her Innocence and synchronize with it. The Level 4 is not inclined to wait around and pursues its mission even against the best efforts of Lavi and Kanda. It's left to Allen to hold the line, but it soon becomes obvious he has no hope of doing it all by himself!"
        assert str(dataset_of_books[4].publisher) == "<Publisher DC Comics>"
        assert isinstance(dataset_of_books[4].publisher, Publisher)
        assert isinstance(dataset_of_books[4].authors[0], Author)
        assert dataset_of_books[4].ebook is False
        assert dataset_of_books[0].ebook is True
        assert dataset_of_books[0].num_pages is None
        assert dataset_of_books[2].num_pages == 146
        assert dataset_of_books[5].num_pages == 206

    def test_read_books_from_file_special_characters(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert dataset_of_books[17].title == "續．星守犬"

class TestMemoryRepository:
    def test_add_book(self, in_memory_repo):
        book = Book(0, 'Parry Hotter')
        in_memory_repo.add_book(book)

        assert in_memory_repo.get_book(0) is book


    def test_get_book(self, in_memory_repo):
        assert isinstance(in_memory_repo.get_book(11827783), Book)


    def test_get_non_existent_book(self, in_memory_repo):
        assert in_memory_repo.get_book(42) is None


    def test_get_all_books(self, in_memory_repo):
        assert isinstance(in_memory_repo.get_all_books(), list)
        assert len(in_memory_repo.get_all_books()) > 0

    def test_search_books_by_title(self, in_memory_repo):
        assert len(in_memory_repo.search_books_by_title("")) == 0
        assert len(in_memory_repo.search_books_by_title("    ")) == 0
        assert len(in_memory_repo.search_books_by_title("vol.")) == 3


    def test_search_books_by_author_name(self, in_memory_repo):
        assert len(in_memory_repo.search_books_by_author_name("")) == 0
        assert len(in_memory_repo.search_books_by_author_name("   ")) == 0
        assert len(in_memory_repo.search_books_by_author_name("mike wol")) == 1


    def test_search_books_by_release_year(self, in_memory_repo):
        assert len(in_memory_repo.search_books_by_release_year("")) == 0
        assert len(in_memory_repo.search_books_by_release_year("   ")) == 0
        assert len(in_memory_repo.search_books_by_release_year("2")) == 15


    def test_search_books_by_publisher_name(self, in_memory_repo):
        assert len(in_memory_repo.search_books_by_publisher_name("")) == 0
        assert len(in_memory_repo.search_books_by_publisher_name("   ")) == 0
        assert len(in_memory_repo.search_books_by_publisher_name("avatar")) == 4


    def test_get_books_by_author(self, in_memory_repo):
        author = in_memory_repo.get_all_authors()[0]
        assert len(in_memory_repo.get_books_by_author(author)) == 1


    def test_get_books_by_non_existent_author(self, in_memory_repo):
        author = Author(666, "Lucifer")
        assert in_memory_repo.get_books_by_author(author) is None


    def test_get_books_from_release_year(self, in_memory_repo):
        assert len(in_memory_repo.get_books_from_release_year(2)) == 0
        assert len(in_memory_repo.get_books_from_release_year(2012)) == 3

    def test_get_all_release_years(self, in_memory_repo):
        assert len(in_memory_repo.get_all_release_years()) == 8


    def test_get_books_by_publisher(self, in_memory_repo):
        publisher = in_memory_repo.get_all_publishers()[0]
        assert len(in_memory_repo.get_books_by_publisher(publisher)) == 1


    def test_get_books_by_non_existent_publisher(self, in_memory_repo):
        publisher = Publisher("Lucas RiedlShah Publications Inc.")
        assert in_memory_repo.get_books_by_publisher(publisher) is None


    def test_add_user_and_get_user(self, in_memory_repo):
        user = User('dave', '123456789')
        in_memory_repo.add_user(user)

        assert in_memory_repo.get_user('dave') is user


    def test_get_non_existent_user(self, in_memory_repo):
        user = in_memory_repo.get_user('prince')
        assert user is None


    def test_add_review_get_book_reviews(self, in_memory_repo):
        book = Book(0, 'Star Trek: The Next Generation')
        user = User("lucas", "ABC123xyz")
        in_memory_repo.add_user(user)
        review = Review(user.user_name, book, "Resistance is futile.", 5)
        in_memory_repo.add_review(review)
        assert len(in_memory_repo.get_book_reviews(book.book_id)) == 1

    def test_get_non_existent_book_reviews(self, in_memory_repo):
        book = Book(0, 'Star Trek: The Next Generation')
        assert len(in_memory_repo.get_book_reviews(book)) == 0
