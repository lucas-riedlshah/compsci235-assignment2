import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from library.adapters import repository
from library.adapters.database_repository import SqlAlchemyRepository
from library.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

DATA_PATH = get_project_root() / "library" / "adapters" / "data"
TEST_DATA_PATH = get_project_root() / "tests" / "data"

DATABASE_URI_IN_MEMORY = 'sqlite://'
DATABASE_URI_FILE = 'sqlite:///library-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.

    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = SqlAlchemyRepository(session_factory)
    repository.populate(TEST_DATA_PATH, repo_instance, database_mode=True)

    yield engine
    
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)

    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = SqlAlchemyRepository(session_factory)
    repository.populate(DATA_PATH, repo_instance, database_mode=True)

    yield session_factory

    metadata.drop_all(engine)

# Unpopulated session
@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)

    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()

    session_factory = sessionmaker(bind=engine)

    yield session_factory()

    metadata.drop_all(engine) 