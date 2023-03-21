import sys
import os
from datetime import date

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    get_contacts_by_firstname,
    get_contacts_by_lastname,
    get_contacts_by_email,
    get_contacts_by_birthday,
    create_contact,
    update_contact,
    remove_contact
)

sys.path.append(os.getcwd())


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a mock session object and a user object with an id of 1.

        :param self: Represent the instance of the object that is being created
        :return: The self
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function.
        It does this by creating a mock session object, and then mocking the query method on that object.
        The mocked query method returns another mock object, which has its filter method mocked to return itself.
        This is done so that we can chain together multiple calls to methods on the same mock objects without having to
        create new ones for each call. Finally, we set up our limit and offset values as well as a list of contacts
        (which are also mocks) which will be returned when all() is called on our final chained-together mock object.

        :param self: Reference the object that is calling the function
        :return: The contacts that are returned from the database
        :doc-author: Trelent
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(offset=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        """
        The test_get_contact_found function tests the get_contact function when a contact is found.
        It does this by creating a mock Contact object, and setting the return value of
        self.session.query().filter().first() to that mock Contact object.
        Then it calls get_contact with an arbitrary contact ID (in this case 1) and passes in our user and session
        objects as arguments, which are used in the function call to get_contact inside of test_get_contact_found.

        :param self: Represent the instance of the class
        :return: The contact object that was found in the database
        :doc-author: Trelent
        """
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        """
        The test_get_contact_not_found function tests the get_contact function when a contact is not found.
            The test_get_contact_not_found function uses the mock library to create a mock session object, and then sets
            that object's query method to return another mock object.  That second mock object has its filter method set
            to return yet another mock, which in turn has its first method set to return None.  This simulates what
            happens when there are no contacts in the database with an id of 1 (the value passed into get_contact).

        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_firstname_found(self):
        """
        The test_get_contact_by_firstname_found function tests the get_contacts_by_firstname function.
        It does this by creating a list of three Contact objects, and then setting the return value of
        self.session.query().filter().all() to that list of contacts. Then it calls get_contacts_by_firstname with
        the first name &quot;art&quot; and compares the result to our expected result (which is just our list of
        contacts). If they are equal, then we know that everything worked as expected.

        :param self: Represent the instance of the class
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_firstname(first_name="derrik", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_firstname_not_found(self):
        """
        The test_get_contact_by_firstname_not_found function tests the get_contacts_by_firstname function
        when a contact is not found. It does this by mocking the session object and returning None when it is called.
        The test then asserts that result of calling get_contacts_by firstname with a first name that doesn't exist in
        the database returns None.

        :param self: Access the attributes and methods of the class in python
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_firstname(first_name="derrik", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_lastname_found(self):
        """
        The test_get_contact_by_lastname_found function tests the get_contacts_by_lastname function.
        It checks that the function returns a list of contacts when it is given a last name and user.


        :param self: Represent the instance of the class
        :return: Contacts
        :doc-author: Trelent
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_lastname(last_name="enko", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_lastname_not_found(self):
        """
        The test_get_contact_by_lastname_not_found function tests the get_contacts_by_lastname function in the
        contacts.py file to ensure that it returns None when a contact with a given last name is not found.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_lastname(last_name="enko", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_email_found(self):
        """
        The test_get_contact_by_email_found function tests the get_contacts_by_email function.
        It does this by mocking a session object and returning a list of contacts when the query is executed.
        The test then asserts that the result of calling get_contacts_by_email with an email address and user is equal
        to the mocked list of contacts.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_email(email="gmail", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_birthday_found(self):
        """
        The test_get_contact_by_birthday_found function tests the get_contacts_by_birthday function.
        It does this by creating a list of contacts, and then setting the return value of
        self.session.query().filter().all() to that list of contacts.
        Then it calls get_contacts_by_birthday with user=self.user and db=self.session as arguments,
        which should return the same list of contacts.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        contacts = [Contact(birthday=date(2000, 4, 18))]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_birthday_not_found(self):
        """
        The test_get_contact_by_birthday_not_found function tests the get_contacts_by_birthday function in the
        contacts.py file
        to ensure that it returns an empty list when no contacts are found with a birthday on the current day.

        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: Contacts
        :doc-author: Trelent
        """
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        """
        The test_create_contact function tests the create_contact function.
        It does so by creating a ContactModel object and passing it to the create_contact function, along with a user and db session.
        The result is then compared to the body of data that was passed in.

        :param self: Represent the instance of the class
        :return: A contactmodel object
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name="Serhii",
            last_name="Romanov",
            email="serrom@test.com",
            phone="123123123",
            birthday=date(2013, 12, 23)
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        """
        The test_remove_contact_found function tests the remove_contact function.
        It does this by creating a mock Contact object, and then setting the return value of
        self.session.query().filter().first to be that mock Contact object (which is what we want).
        Then it calls remove_contact with contact_id= 1, user = self.user (a mocked User), and db = self session (a mocked Session).
        The result should be equal to our mock Contact object.

        :param self: Represent the instance of the class
        :return: The contact object
        :doc-author: Trelent
        """
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        """
        The test_remove_contact_not_found function tests the remove_contact function in the contacts.py file.
        The test_remove_contact_not_found function is a coroutine that takes no arguments and returns nothing.
        The test checks to see if the remove contact function returns None when it tries to delete a contact that does not exist.

        :param self: Refer to the object itself
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        """
        The test_update_contact_found function tests the update_contact function.
        It checks if the contact is found and updated correctly.

        :param self: Access the attributes and methods of the class in python
        :return: The contact object
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name="Serhii",
            last_name="Romanov",
            email="serrom@test.com",
            phone="123123123",
            birthday=date(2013, 12, 23)
        )
        contact = ContactModel(
            first_name="Yuriy",
            last_name="Prosto",
            email="proyir@test.com",
            phone="123123123",
            birthday=date(2010, 2, 13)
        )
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        """
        The test_update_contact_not_found function tests the update_contact function when a contact is not found.
            The test_update_contact_not_found function uses the following fixtures:
                - self.user, which is a UserModel object with id=2 and email=&quot;test@gmail.com&quot;
                - self.session, which is an instance of MagicMock() that represents a database session

        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name="Serhii",
            last_name="Romanov",
            email="serrom@test.com",
            phone="123123123",
            birthday=date(2013, 12, 23)
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
