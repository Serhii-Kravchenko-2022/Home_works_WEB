import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base
from src.database.connect_db import get_db

sys.path.append(os.getcwd())

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    """
    The session function is a fixture that will ensure that a new database is
    created for each test, and it will be torn down when the test ends. This
    allows you to have complete isolation between your tests. The session object
    is also scoped so that it only lives for the duration of a single test, which
    means you don't need to worry about deleting data from one test affecting other
    tests.

    :return: A session object
    :doc-author: Trelent
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    """
    The client function is a fixture that will be called to create a test client
    for your application. It takes the Flask app as an argument and returns a
    TestClient instance, which you can then use to make requests in your tests.


    :param session: Override the get_db function
    :return: A testclient instance, which is used to make http requests in the tests
    :doc-author: Trelent
    """
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    """
    The user function returns a dictionary with the following keys:
        username, email, password.


    :return: A dictionary with the username, email and password
    :doc-author: Trelent
    """
    return {"username": "deadpool", "email": "deadpool@example.com", "password": "123456789"}