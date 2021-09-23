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

    if filter_category == "books":
        books = search_books(repo, query)
    elif filter_category == "authors":
        authors = search_authors(repo, query)
    elif filter_category == "publishers":
        publishers = search_publishers(repo, query)
    else:
        books = search_books(repo, query)[:4]
        authors = search_authors(repo, query)[:4]
        publishers = search_publishers(repo, query)[:4]

    return render_template('search/search.html', recommend_all_books_from_year=recommend_all_books_from_year, query=query, filter_category=filter_category, books=books, authors=authors, publishers=publishers)
