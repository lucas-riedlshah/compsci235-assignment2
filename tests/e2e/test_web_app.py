import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/register',
        data={'user_name': 'deargod', 'password': 'Idontbelieve1986'}
    )
    assert response.headers['Location'] == 'http://localhost/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Your username is required'),
    ('cj', '', b'Your username is too short'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Your password must be at least 8 characters, and contain at least one upper case letter,\
            one lower case letter and one digit')
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_register_name_already_taken(client):
    response = client.post(
        '/register',
        data={'user_name': 'trivial_name', 'password': 'Trivial_password123'}
    )
    response = client.post(
        '/register',
        data={'user_name': 'trivial_name', 'password': 'Novel_password456'}
    )
    assert b'This username is already taken. Please choose a different one.' in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/login').status_code
    assert status_code == 200

    # Register a user
    auth.register()

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'takashi'


def test_logout(client, auth):
    auth.register()
    auth.login()
    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_name' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Comic Book Library' in response.data


def test_login_required_to_review_book(client):
    response = client.post(
        '/book?id=707611',
        data={'rating': 3, 'review_text': 'very cool book'}
    )
    assert response.headers['Location'] == 'http://localhost/login'

def test_review_book(client, auth):
    auth.register()
    auth.login()

    response = client.post(
        '/book?id=707611',
        data={'rating': 3, 'review_text': 'very cool book'}
    )
    assert response.headers['Location'] == 'http://localhost/book?id=707611'

    # Check that review is showing up on the book page.
    response = client.get('/book?id=707611')
    assert b'very cool book' in response.data

def test_book_without_id(client):
    response = client.get('/book')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/books'

def test_book_with_id(client):
    response = client.get('/book?id=707611')
    assert response.status_code == 200
    assert b'Superman Archives, Vol. 2' in response.data

def test_books(client):
    response = client.get('/books')
    assert b'Books' in response.data

def test_books_with_extra_parameters(client):
    response = client.get('/books?year=1997&author=81563&publisher=DC+Comics')
    assert b'Jerry Siegel' in response.data
    assert b'1997' in response.data
    assert b'DC Comics' in response.data