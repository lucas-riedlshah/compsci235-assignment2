import pytest

from library.authentication.services import *


def test_add(in_memory_repo):
    new_user_name = "lucas"
    new_password = "123ABCxyz"
    add_user(in_memory_repo, new_user_name, new_password)

    user_as_dict = get_user(in_memory_repo, new_user_name)

    assert user_as_dict["user_name"] == new_user_name
    assert user_as_dict["password"].startswith(
        "pbkdf2:sha256:")  # Check password is encrypted

    with pytest.raises(NameNotUniqueException):
        add_user(in_memory_repo, new_user_name, new_password)


def test_get_user(in_memory_repo):
    new_user_name = "lucas"
    new_password = "123ABCxyz"

    with pytest.raises(UnknownUserException):
        get_user(in_memory_repo, "lucas")

    add_user(in_memory_repo, new_user_name, new_password)

    assert get_user(in_memory_repo, new_user_name)[
        "user_name"] == new_user_name


def test_authentication_user(in_memory_repo):
    new_user_name = "ashley_bloomfield"
    new_password = "123ABCxyz"

    add_user(in_memory_repo, new_user_name, new_password)

    with pytest.raises(AuthenticationException):
        authenticate_user(in_memory_repo, new_user_name, "P4ssw0rd")

    authenticate_user(in_memory_repo, new_user_name, new_password)
