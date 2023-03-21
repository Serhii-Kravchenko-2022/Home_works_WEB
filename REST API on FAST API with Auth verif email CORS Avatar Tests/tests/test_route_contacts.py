import sys
import os

from unittest.mock import MagicMock, patch
import pytest

from src.database.models import User
from src.services.auth import auth_service

sys.path.append(os.getcwd())


@pytest.fixture()
def token(client, user, session, monkeypatch):
    """
    The token function is used to create a token for the user.
        It takes in the client, user, session and monkeypatch as arguments.
        The mock_send_email function is created using MagicMock().
        The setattr() method sets an attribute value of an object.
            Here it sets the send email function with mock_send_email function.

    :param client: Make requests to the api
    :param user: Create a user in the database
    :param session: Create a new session for the test
    :param monkeypatch: Mock the send_email function
    :return: A token
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.confirmed_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_get_contacts_not_found(client, token):
    """
    The test_get_contacts_not_found function tests the get_contacts function in the contacts_service module.
    It does this by mocking out the redis cache and setting it to return None when called.
    Then, it makes a GET request to /api/contacts with an Authorization header containing a valid token.
    The response should be 404 Not Found, and its JSON body should contain &quot;Not found&quot; as its detail.

    :param client: Make requests to the api
    :param token: Pass in the token that is generated from the test_get_contacts function
    :return: A 404 response with a detail of &quot;not found&quot;
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"


def test_create_contact(client, token):
    """
    The test_create_contact function tests the creation of a contact.
    It does so by first mocking the redis_cache object in auth_service, and then setting its get method to return None.
    This is done because we want to test that our API can create a new contact even if there is no cache available.
    Next, it sends an HTTP POST request with some JSON data containing information about the new contact (first name,
    last name, email address etc.). The response from this request should be 200 OK and contain JSON data with
    all_of the fields we sent in our POST request plus an id field which was generated automatically by SQLAl

    :param client: Make requests to the flask application
    :param token: Pass the token to the test function
    :return: The following:
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={
                "first_name": "Serhii",
                "last_name": "Romanov",
                "email": "serrom@test.com",
                "phone": "123123123",
                "birthday": "2033-12-23"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]["first_name"] == "Serhii"
        assert data[0]["last_name"] == "Romanov"
        assert data[0]["email"] == "serrom@test.com"
        assert data[0]["phone"] == "123123123"
        assert "id" in data


def test_get_contacts(client, token):
    """
    The test_get_contacts function tests the GET /api/contacts endpoint.
    It does so by first mocking out the redis_cache object in auth_service, and then setting its get method to
    return None.
    This is done because we want to test that our API will call this function when it needs to retrieve a user's
    contacts from Redis cache.
    We then make a request with an Authorization header containing our token, which should be valid for this
    endpoint (see auth_service).
    If all goes well, we should receive a 200 response code and some JSON data representing the user's contacts.

    :param client: Make requests to the flask application
    :param token: Authenticate the user
    :return: A list of contacts
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "Serhii"
        assert "id" in data[0]


def test_get_contact_by_id(client, token):
    """
    The test_get_contact_by_id function tests the get_contact_by_id endpoint.
    It does so by first patching the redis cache to return None, which will cause a call to be made to the database.
    Then it makes a GET request with an Authorization header containing a valid token and checks that:
        - The response status code is 200 OK; and
        - The data returned in JSON format contains all of Cristiano Ronaldo's contact details.

    :param client: Make requests to the api
    :param token: Authenticate the user
    :return: The contact with id 1
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_id/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]["first_name"] == "Serhii"
        assert data[0]["last_name"] == "Romanov"
        assert data[0]["email"] == "serrom@test.com"
        assert data[0]["phone"] == "123123123"
        assert "id" in data


def test_get_contact_by_id_not_found(client, token):
    """
    The test_get_contact_by_id_not_found function tests the get_contact_by_id endpoint.
    It does so by mocking the redis cache and returning None when it is called.
    The test then makes a request to the endpoint with an id that doesn't exist in our database, and asserts that we
    receive a 404 response.

    :param client: Make a request to the api
    :param token: Pass the token to the test function
    :return: A 404 status code and a message
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_id/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_update_contact(client, token):
    """
    The test_update_contact function tests the update contact endpoint.
        It does so by first mocking the redis_cache object in auth_service, and then setting its get method to
        return None.
        Then it makes a PUT request to /api/contacts/&lt;contact id&gt; with a JSON body containing all_of_the fields
        that are required for updating a contact, as well as an Authorization header containing our token.
        Finally, it asserts that we receive back an HTTP 200 response code from our server (indicating success),
        and then checks if all of the fields in our JSON body were updated correctly.

    :param client: Make requests to the flask application
    :param token: Authenticate the user
    :return: A 200 status code and the data that was modified
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "first_name": "Serhii",
                "last_name": "Romanov",
                "email": "serrom@test.com",
                "phone": "123123123",
                "birthday": "2033-12-23"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]["first_name"] == "Serhii"
        assert data[0]["last_name"] == "Romanov"
        assert data[0]["email"] == "serrom@test.com"
        assert data[0]["phone"] == "123123123"


def test_update_contact_not_found(client, token):
    """
    The test_update_contact_not_found function tests the update contact endpoint when a user tries to update a contact
    that does not exist. The test_update_contact_not_found function uses the client fixture to make an HTTP PUT request
    with json data and headers containing an authorization token. The test asserts that the response status code
    is 404, which indicates that no resource was found at this endpoint. The response text is also printed in case
    of failure.

    :param client: Make requests to the flask app
    :param token: Pass the token to the test function
    :return: A 404 status code with a message
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                "first_name": "Serhii",
                "last_name": "Romanov",
                "email": "serrom@test.com",
                "phone": "123123123",
                "birthday": "2033-12-23"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"


def test_get_contacts_with_birthday(client, token):
    """
    The test_get_contacts_with_birthday function tests the get_contacts_with_birthday function in the contacts.py file.
    The test uses a client to make a GET request to /api/contacts/birthday/. The response is then checked for status
    code 200,  which means that the request was successful and returned data as expected. The data is then checked
    for correctness.

    :param client: Make requests to the api
    :param token: Authenticate the user
    :return: A list of contacts with a birthday
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/birthday/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["first_name"] == "Serhii"
        assert data[0]["last_name"] == "Romanov"
        assert data[0]["email"] == "serrom@test.com"
        assert data[0]["phone"] == "123123123"


def test_delete_contact(client, token):
    """
    The test_delete_contact function tests the_delete contact endpoint.
        It does this by first mocking out the redis_cache object in auth_service, and then setting its get method to return None.
        Then it makes a DELETE request to /api/contacts/&lt;contact id&gt; with an Authorization header containing a valid JWT token.
        The test asserts that the response status code is 200.

    :param client: Make requests to the flask application
    :param token: Authenticate the user
    :return: A 200 status code
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text


def test_repeat_delete_contact(client, token):
    """
    The test_repeat_delete_contact function tests the repeat delete contact endpoint.
        It does this by mocking the redis_cache object and setting its get method to return None.
        Then it sends a DELETE request to /api/contacts/&lt;contact_id&gt; with an Authorization header containing a
        valid token. The response should have status code 404, and its JSON body should contain &quot;Not found&quot;
        in the detail field.

    :param client: Send requests to the api
    :param token: Pass the token to the function
    :return: A 404 error
    :doc-author: Trelent
    """
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found"
