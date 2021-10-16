from sqlalchemy import Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey

from sqlalchemy.orm import mapper, relationship

from library.domain import *

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True),
    Column('password', String(255))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255)),
    Column('book_id', ForeignKey('books.id')),
    Column('rating', Integer),
    Column('review_text', String(1024)),
    Column('timestamp', DateTime, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024)),
    Column('release_year', Integer),
    Column('isbn', String(255)),
    Column('publisher_id', ForeignKey('publishers.id'))
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('full_name', String(255), nullable=False)
)

book_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id')),
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255))
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
    })
    mapper(Review, reviews_table, properties={
        '_Review__user_name': reviews_table.c.user_name,
        '_Review__book': relationship(Book),
        '_Review__rating': reviews_table.c.rating,
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__isbn': books_table.c.isbn,
        '_Book__authors': relationship(Author, secondary=book_authors_table),
        '_Book__publisher': relationship(Publisher)
    })
    mapper(Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.full_name,
    })
    mapper(Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
    })
