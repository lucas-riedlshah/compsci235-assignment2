import re

from library.adapters.repository import AbstractRepository
from library.utilities import author_to_dict, book_to_dict, publisher_to_dict


def search_books(repo: AbstractRepository, query: str):
    # remove any non-word or whitespace characters using regex. (aka remove punctuation)
    query = re.sub(r'[^\w\s]', '', query).strip().lower()
    if len(query) == 0:
        return []
    query_words = query.split(" ")
    books = []
    distances = []  # A list of integers describing how similar the book's title is to the search query
    for book in repo.get_all_books():
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
    return [book_to_dict(book) for book in books]


def search_authors(repo: AbstractRepository, query: str):
    # remove any non-word or whitespace characters using regex. (aka remove punctuation)
    query = re.sub(r'[^\w\s]', '', query).strip().lower()
    if len(query) == 0:
        return []
    query_words = query.split(" ")
    authors = []
    distances = []  # A list of integers describing how similar the author's title is to the search query
    for author in repo.get_all_authors():
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
    return [author_to_dict(authors) for authors in authors]


def search_publishers(repo: AbstractRepository, query: str):
    # remove any non-word or whitespace characters using regex. (aka remove punctuation)
    query = re.sub(r'[^\w\s]', '', query).strip().lower()
    if len(query) == 0:
        return []
    query_words = query.split(" ")
    publishers = []
    distances = []  # A list of integers describing how similar the publisher's title is to the search query
    for publisher in repo.get_all_publishers():
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
    return [publisher_to_dict(publisher) for publisher in publishers]
