import sys
import os
from unittest.mock import MagicMock


from src.database.models import User

sys.path.append(os.getcwd())


def test_create_user(client, user, monkeypatch):
    """
    The test_create_user function tests the /api/auth/signup endpoint.
    It does so by creating a user and then checking that the response is 201 (created)
    and that the email address of the created user matches what was sent in.

    :param client: Make requests to the app
    :param user: Pass in the user data to create a new user
    :param monkeypatch: Mock the send_email function
    :return: A 201 status code, the user's email and an id
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.confirmed_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
        It does this by creating a user, then attempting to create the same user again.
        The second attempt should fail with an HTTP 409 status code.

    :param client: Make a request to the api
    :param user: Pass the user data to the test function
    :return: A 409 error, which means that the request could not be processed because of conflict in the current state of the resource
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    """
    The test_login_user_not_confirmed function tests that a user cannot login if they have not confirmed their email.
    It does this by first creating a new user, then attempting to log in with the credentials of that user.
    The test asserts that the response status code is 401 (Unauthorized), and also checks for an error message.

    :param client: Test the api
    :param user: Create a user in the database
    :return: A 401 status code and a message that the email is not confirmed
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_login_user(client, session, user):
    """
    The test_login_user function tests the login endpoint.
    It does this by first creating a user, then confirming that user's account.
    Then it attempts to log in with the correct credentials and asserts that it receives a 200 response code.

    :param client: Make requests to the application
    :param session: Access the database
    :param user: Create a user in the database
    :return: A token_type of bearer
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    """
    The test_login_wrong_password function tests the login endpoint with a wrong password.
    It should return a 401 status code and an error message.

    :param client: Make requests to the flask application
    :param user: Create a user in the database
    :return: 401, response
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_login_wrong_email(client, user):
    """
    The test_login_wrong_email function tests the login endpoint with a wrong email.
    It should return a 401 status code and an error message.

    :param client: Make requests to the flask application
    :param user: Pass the user data to the test function
    :return: A 401 status code, it also returns a json object with the key detail and value invalid email
    :doc-author: Trelent
    """
    response = client.post(
        "/api/auth/login",
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
