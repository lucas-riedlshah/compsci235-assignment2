"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template

import library.adapters.repository as repository
from library.adapters.repository import populate
from library.adapters.memory_repository import MemoryRepository


def create_app(test_config = None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repository.repo_instance = MemoryRepository()
    populate(data_path, repository.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .books import books
        app.register_blueprint(books.books_blueprint)

        from .authors import authors
        app.register_blueprint(authors.authors_blueprint)

        from .publishers import publishers
        app.register_blueprint(publishers.publishers_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app