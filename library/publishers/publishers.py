from flask import Blueprint, request, render_template, url_for, redirect

from .services import *
from library.adapters.repository import repo_instance as repo

publishers_blueprint = Blueprint('publishers_bp', __name__)


@publishers_blueprint.route('/publishers', methods=['GET'])
def publishers():
    try:
        page = int(request.args.get('page') or 1)
    except ValueError:
        page = 1

    if page < 1:
        page = 1

    publishers = get_nth_publishers_page(repo, page)
    page_count = get_publishers_page_count(repo)
    first_page_url = url_for('publishers_bp.publishers', page=1)
    next_page_url = url_for('publishers_bp.publishers',
                            page=page + 1) if page < page_count else None
    previous_page_url = url_for(
        'publishers_bp.publishers', page=page - 1) if page > 1 else None
    last_page_url = url_for('publishers_bp.publishers', page=page_count)
    return render_template(
        'publishers/all_publishers.html',
        publishers=publishers,
        first_page_url=first_page_url,
        next_page_url=next_page_url,
        previous_page_url=previous_page_url,
        last_page_url=last_page_url
    )
    return render_template('publishers/all_publishers.html')


@publishers_blueprint.route('/publisher', methods=['GET'])
def publisher():
    name = request.args.get('name')
    if name is None:
        return redirect(url_for('home_bp.home'))

    try:
        page = int(request.args.get('page') or 1)
    except ValueError:
        page = 1
    if page < 1:
        page = 1

    publisher = get_publisher(repo, name)
    if publisher is None:
        return redirect(url_for('home_bp.home'))

    books = get_nth_books_by_publisher_page(repo, publisher.name, page)

    page_count = get_books_by_publisher_page_count(repo, publisher.name)
    first_page_url = url_for('publishers_bp.publisher', name=name, page=1)
    next_page_url = url_for('publishers_bp.publisher', name=name,
                            page=page + 1) if page < page_count else None
    previous_page_url = url_for(
        'publishers_bp.publisher', name=name, page=page - 1) if page > 1 else None
    last_page_url = url_for('publishers_bp.publisher', name=name, page=page_count)

    return render_template(
        'publishers/publisher.html',
        publisher=publisher,
        books=books,
        first_page_url=first_page_url,
        next_page_url=next_page_url,
        previous_page_url=previous_page_url,
        last_page_url=last_page_url
    )
