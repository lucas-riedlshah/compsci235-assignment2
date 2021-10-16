"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import library.adapters.repository as repository
from library.adapters.repository import populate
from library.adapters.memory_repository import MemoryRepository
from library.adapters.database_repository import SqlAlchemyRepository
from library.adapters.orm import metadata, map_model_to_tables


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        repository.repo_instance = MemoryRepository()
        populate(data_path, repository.repo_instance)
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(
            database_uri,
            connect_args={'check_same_thread': False},
            poolclass=NullPool,
            echo=database_echo
        )

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        repository.repo_instance = SqlAlchemyRepository(session_factory)
        
        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            clear_mappers()

            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())

            map_model_to_tables()

            populate(data_path, repository.repo_instance, database_mode=True)
        else:
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .books import books
        app.register_blueprint(books.books_blueprint)

        from .authors import authors
        app.register_blueprint(authors.authors_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .publishers import publishers
        app.register_blueprint(publishers.publishers_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        @app.before_request
        def before_http_request():
            if isinstance(repository.repo_instance, SqlAlchemyRepository):
                repository.repo_instance.reset_session()
            
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repository.repo_instance, SqlAlchemyRepository):
                repository.repo_instance.close_session()

    return app
