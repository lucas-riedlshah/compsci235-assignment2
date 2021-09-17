from flask import Blueprint, request, render_template, url_for, redirect

from .services import *
from library.adapters.repository import repo_instance as repo

books_blueprint = Blueprint('books_bp', __name__)


@books_blueprint.route('/books', methods=['GET'])
def books():
    try:
        page = int(request.args.get('page') or 1)
    except ValueError:
        page = 1

    if page < 1:
        page = 1

    books = get_nth_books_page(repo, page)
    page_count = get_books_page_count(repo)
    first_page_url = url_for('books_bp.books', page=1)
    next_page_url = url_for('books_bp.books', page=page + 1) if page < page_count else None
    previous_page_url = url_for('books_bp.books', page=page - 1) if page > 1 else None
    last_page_url = url_for('books_bp.books', page=page_count)
    return render_template(
        'books/all_books.html',
        books=books,
        first_page_url=first_page_url,
        next_page_url=next_page_url,
        previous_page_url=previous_page_url,
        last_page_url=last_page_url
    )

@books_blueprint.route('/book', methods=['GET'])
def book():
    book_id = request.args.get('id')
    if book_id is None:
        return redirect(url_for('home_bp.home'))
    try:
        book_id = int(book_id)
    except ValueError:
        return redirect(url_for('home_bp.home'))
    book = get_book(repo, book_id)
    if book is None:
        return redirect(url_for('home_bp.home'))
    return render_template('books/book.html', book=book)