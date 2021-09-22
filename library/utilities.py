from library.domain import Author, Book, Publisher, Review, User


def author_to_dict(author: Author):
    return {
        'unique_id': author.unique_id,
        'full_name': author.full_name,
    }


def book_to_dict(book: Book):
    return {
        'title': book.title,
        'description': book.description,
        'publisher': publisher_to_dict(book.publisher),
        'authors': [author_to_dict(author) for author in book.authors],
        'release_year': book.release_year,
        'isbn': book.isbn,
        'book_id': book.book_id
    }


def publisher_to_dict(publisher: Publisher):
    return {
        "name": publisher.name
    }


def review_to_dict(review: Review):
    return {
        'user_name': review.user_name,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }


def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password
    }
    return user_dict
