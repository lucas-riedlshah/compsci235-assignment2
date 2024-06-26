from pathlib import Path
import pytest

from library import create_app
from library.adapters import repository
from library.adapters.memory_repository import MemoryRepository
from library.adapters.jsondatareader import BooksJSONReader

from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()


@pytest.fixture
def read_books_and_authors():
    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'

    # we use a method from a utils file in the root folder to figure out the root
    # this way testing code is always finding the right path to the data files
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)
    reader.read_json_files()
    return reader.dataset_of_books

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='takashi', password='ABC123xyz'):
        return self.__client.post(
            'register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='takashi', password='ABC123xyz'):
        return self.__client.post(
            'login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
