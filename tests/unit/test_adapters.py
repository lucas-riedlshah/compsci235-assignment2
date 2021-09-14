from pathlib import Path
import pytest

from utils import get_project_root

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
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
