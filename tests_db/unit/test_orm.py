import pytest
from sqlalchemy.exc import IntegrityError

from library.domain import User, Review, Book, Author, Publisher

def test_load_user(empty_session):
    empty_session.execute('INSERT INTO users (user_name, password) VALUES ("amine", "123ABCsecure")')
    empty_session.execute('INSERT INTO users (user_name, password) VALUES ("theophilus_london", "888")')
    assert empty_session.query(User).all() == [User("amine", "123ABCsecure"), User("theophilus_london", "888")]

def test_save_user(empty_session):
    empty_session.add(User("mexican_institute_of_sound", "distritofederal"))
    empty_session.commit()
    assert list(empty_session.execute('SELECT user_name, password FROM users')) == [("mexican_institute_of_sound", "distritofederal")]

def test_save_users_with_same_name(empty_session):
    empty_session.add(User("pinkfloyd", "Breathe (In The Air)"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        empty_session.add(User("pinkfloyd", "The Piper At The Gates Of Dawn"))
        empty_session.commit()

def test_load_author(empty_session):
    empty_session.execute(
        'INSERT INTO authors (id, full_name) \
         VALUES (100, "Nirvana")'
    )
    assert empty_session.query(Author).one() == Author(100, "Nirvana")

def test_save_author(empty_session):
    author = Author(2021, "Sufjan Stevens")
    empty_session.add(author)
    empty_session.commit()

    assert list(empty_session.execute('SELECT id, full_name FROM authors')) == [(2021, 'Sufjan Stevens')]

def test_load_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name) \
         VALUES ("future classic")'
    )
    assert empty_session.query(Publisher).one() == Publisher('future classic')

def test_save_publisher(empty_session):
    publisher = Publisher('Murdoc')
    empty_session.add(publisher)
    empty_session.commit()

    assert list(empty_session.execute('SELECT name FROM publishers')) == [('Murdoc',)]

def test_load_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (id, title, description, release_year, isbn) \
         VALUES (200, "Flamboyant", "An album by Dorian Electra.", 2019, "123XYZ")'
    )
    book = Book(200, "Flamboyant")
    book.description = "An album by Dorian Electra."
    book.release_year = 2019
    book.isbn = "123XYZ"
    assert empty_session.query(Book).one() == book

def test_save_books(empty_session):
    book = Book(300, "Gold Soul Theory")
    book.description = "A song by The Underachievers."
    book.release_year = 2013
    book.isbn = "1234ABCD"
    empty_session.add(book)
    empty_session.commit()
    assert list(empty_session.execute('SELECT title, description FROM books')) == [("Gold Soul Theory", "A song by The Underachievers.")]

def test_load_review(empty_session):
    book = Book(2095, "Time")
    review = Review('elo', book, "A good album.", 4)

    empty_session.add(book)
    empty_session.commit()
    empty_session.execute(
        'INSERT INTO reviews (user_name, book_id, rating, review_text, timestamp) \
         VALUES ("elo", :book_id, 4, "A good album.", :timestamp)',
        {'book_id': book.book_id, 'timestamp': review.timestamp}
    )

    assert empty_session.query(Review).one() == review

def test_save_review(empty_session):
    book = Book(2095, "Time")
    review = Review('elo', book, "Such a good album.", 4)
    
    empty_session.add(book)
    empty_session.add(review)
    empty_session.commit()

    assert list(empty_session.execute('SELECT user_name, book_id, review_text FROM reviews')) == [("elo", 2095, "Such a good album.")]

def test_load_book_with_authors(empty_session):
    empty_session.execute(
        'INSERT INTO books (id, title) VALUES (555, "J.S. Bach: Orchestral Suite No.3 in D Major, BWV 1068 - 2. Air")'
    )
    empty_session.execute(
        'INSERT INTO authors (id, full_name) VALUES (111, "Münchener Bach-Orchester"), (333, "Karl Richter")'
    )
    empty_session.execute(
        'INSERT INTO book_authors (book_id, author_id) VALUES (555, 111), (555, 333)'
    )

    assert empty_session.query(Book).one().authors == [Author(111, 'Münchener Bach-Orchester'), Author(333, 'Karl Richter')]

def test_save_book_with_authors(empty_session):
    book = Book(7, "The Pink Phantom")
    authors = [Author(123, "Gorillaz"), Author(456, "Elton John"), Author(789, "6LACK")]
    for author in authors:
        book.add_author(author)

    empty_session.add(book)
    empty_session.commit()

    assert list(empty_session.execute('SELECT book_id, author_id from book_authors')) == [(7, 123), (7, 456), (7, 789)]