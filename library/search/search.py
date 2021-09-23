from flask import Blueprint, request, render_template, url_for, redirect

from .services import *
from library.adapters.repository import repo_instance as repo

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('q') or ""
    filter_category = request.args.get('filter') or ""

    recommend_all_books_from_year = False
    if query.isnumeric() and int(query) in repo.get_all_release_years():
        recommend_all_books_from_year = True

    books = []
    authors = []
    publishers = []
    book_result_count = 0
    author_result_count = 0
    publisher_result_count = 0

    if filter_category == "books":
        books = search_books(repo, query)
        book_result_count = len(books)
    elif filter_category == "authors":
        authors = search_authors(repo, query)
        author_result_count = len(authors)
    elif filter_category == "publishers":
        publishers = search_publishers(repo, query)
        publisher_result_count = len(publishers)
    else:
        books = search_books(repo, query)
        authors = search_authors(repo, query)
        publishers = search_publishers(repo, query)

        book_result_count = len(books)
        author_result_count = len(authors)
        publisher_result_count = len(publishers)

        books = books[:4]
        authors = authors[:4]
        publishers = publishers[:4]

    return render_template(
        'search/search.html',
        recommend_all_books_from_year=recommend_all_books_from_year,
        query=query,
        filter_category=filter_category,
        book_result_count=book_result_count,
        author_result_count=author_result_count,
        publisher_result_count=publisher_result_count,
        books=books,
        authors=authors,
        publishers=publishers
    )
