from flask import Blueprint, request, render_template, url_for, redirect

from .services import *
from library.adapters.repository import repo_instance as repo

authors_blueprint = Blueprint('authors_bp', __name__)


@authors_blueprint.route('/authors', methods=['GET'])
def authors():
    try:
        page = int(request.args.get('page') or 1)
    except ValueError:
        page = 1

    if page < 1:
        page = 1

    authors = get_nth_authors_page(repo, page)
    page_count = get_authors_page_count(repo)
    first_page_url = url_for('authors_bp.authors', page=1)
    next_page_url = url_for('authors_bp.authors',
                            page=page + 1) if page < page_count else None
    previous_page_url = url_for(
        'authors_bp.authors', page=page - 1) if page > 1 else None
    last_page_url = url_for('authors_bp.authors', page=page_count)
    return render_template(
        'authors/all_authors.html',
        authors=authors,
        first_page_url=first_page_url,
        next_page_url=next_page_url,
        previous_page_url=previous_page_url,
        last_page_url=last_page_url
    )
