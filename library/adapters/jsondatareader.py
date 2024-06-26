import json

from library.domain import Publisher, Author, Book


class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []

    @property
    def dataset_of_books(self) -> list[Book]:
        return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json


    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()

        publishers = {}
        authors = {}

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            book_instance.isbn = book_json['isbn']
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])
            
            publisher_name = book_json['publisher']
            if publisher_name not in publishers:
                publishers[publisher_name] = Publisher(publisher_name)
            book_instance.publisher = publishers[publisher_name]

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:

                numerical_id = int(author_id['author_id'])

                if numerical_id not in authors:
                    # We assume book authors are available in the authors file,
                    # otherwise more complex handling is required.
                    author_name = None
                    author_average_rating = None
                    author_ratings_count = None
                    for author_json in authors_json:
                        if int(author_json['author_id']) == numerical_id:
                            author_name = author_json['name']
                            author_average_rating = float(author_json['average_rating'])
                            author_ratings_count = int(author_json['ratings_count'])
                    author = Author(numerical_id, author_name)
                    author.average_rating = author_average_rating
                    author.ratings_count = author_ratings_count
                    authors[numerical_id] = author

                book_instance.add_author(authors[numerical_id])


            self.__dataset_of_books.append(book_instance)
