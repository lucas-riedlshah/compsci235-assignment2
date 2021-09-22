from werkzeug.security import generate_password_hash, check_password_hash

from library.adapters.repository import AbstractRepository
from library.domain import User
from library.utilities import user_to_dict


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(repo: AbstractRepository, user_name: str, password: str):
    if repo.get_user(user_name) is not None:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)

    repo.add_user(User(user_name, password_hash))


def get_user(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name.lower())
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(repo: AbstractRepository, user_name: str, password: str):
    authenticated = False
    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException
