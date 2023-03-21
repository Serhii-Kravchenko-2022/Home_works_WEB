import sys
import os

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    confirmed_email,
)

sys.path.append(os.getcwd())


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session object and a body object that will be used in the tests.

        :param self: Represent the instance of the class
        :return: The instance of the class
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            username="Serhii",
            email="serhi@test.com",
            password="123456"
        )

    async def test_get_user_by_email(self):
        """
        The test_get_user_by_email function tests the get_user_by_email function.
        It does this by creating a mock user object and setting the return value of
        the session query filter to be that mock user. Then it calls get_user_by email,
        and asserts that the result is equal to our mocked user.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: The user
        :doc-author: Trelent
        """
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test1@test.com", db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function.
        It does this by creating a user with the body of self.body, which is defined in setUpClass().
        The result is then compared to what we expect it to be.

        :param self: Represent the instance of the class
        :return: A user object with the attributes username, email, password and id
        :doc-author: Trelent
        """
        body = self.body
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email(self):
        """
        The test_confirmed_email function tests the confirmed_email function.
        It creates a user with the create_user function, then confirms that user's email with the confirmed_email function.
        Then it gets that user from the database and checks to see if their 'confirmed' field is True.

        :param self: Represent the instance of the class
        :return: The result of the get_user_by_email function
        :doc-author: Trelent
        """
        body = self.body
        await create_user(body=body, db=self.session)
        await confirmed_email(email=body.email, db=self.session)
        result = await get_user_by_email(email=body.email, db=self.session)
        self.assertEqual(result.confirmed, True)


if __name__ == '__main__':
    unittest.main()
