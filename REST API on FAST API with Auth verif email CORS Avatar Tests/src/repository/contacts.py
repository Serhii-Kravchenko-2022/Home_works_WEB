from typing import List
from datetime import timedelta, date

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas import ContactModel


async def get_contacts(offset: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param offset: int: Specify the number of records to skip before returning results
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user's contacts from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(offset).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this Contact.

    :param contact_id: int: Specify the id of the contact to be returned
    :param user: User: Get the user's id
    :param db: Session: Access the database
    :return: The first contact with the given id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def get_contacts_by_firstname(first_name: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_firstname function returns a list of contacts that match the first name provided.
        Args:
            first_name (str): The first name to search for in the database.
            user (User): The user who is making this request. This is used to determine if they have access to this resource or not.
            db (Session): A connection to our database, which we use for querying and updating data.

    :param first_name: str: Define the first name of a contact
    :param user: User: Get the user's id from the database
    :param db: Session: Pass in the database session to be used for querying
    :return: A list of contacts that match the first name
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.first_name.like(f'%{first_name}%')).all()


async def get_contacts_by_lastname(last_name: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_lastname function returns a list of contacts that match the last name provided.
        Args:
            last_name (str): The last name to search for in the database.
            user (User): The user who is making this request. This is used to ensure that only contacts belonging to
            this  user are returned, and not all contacts with the given first name in the database.

    :param last_name: str: Filter the contacts by last name
    :param user: User: Get the user_id of the current user
    :param db: Session: Connect to the database
    :return: A list of contacts that match the last name
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.last_name.like(f'%{last_name}%'))).all()


async def get_contacts_by_email(email: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_email function takes in an email string and a user object,
    and returns a list of contacts that match the given email.


    :param email: str: Filter the contacts by email
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that match the email address
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.email.like(f'%{email}%'))).all()


async def get_contacts_by_birthday(user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_birthday function returns a list of contacts that have birthdays within the next 7 days.
    The function takes in two parameters: user and db. The user parameter is an object of type User, which contains
    the id of the current logged-in user. The db parameter is an object of type Session, which represents a database
    session.

    :param user: User: Get the user id from the user object
    :param db: Session: Connect to the database
    :return: A list of contacts whose birthdays are in the next 7 days
    :doc-author: Trelent
    """
    date_from = date.today()
    date_to = date.today() + timedelta(days=7)
    this_year = date_from.year
    next_year = date_from.year + 1
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                            or_(
                                                func.to_date(
                                                    func.concat(func.to_char(Contact.birthday, "DDMM"), this_year),
                                                    "DDMMYYYY").between(date_from,
                                                                        date_to),
                                                func.to_date(
                                                    func.concat(func.to_char(Contact.birthday, "DDMM"), next_year),
                                                    "DDMMYYYY").between(date_from,
                                                                        date_to),
                                            ))
                                       ).all()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database

    :return: A contact object
    """
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated ContactModel object with new values for first_name, last_name, email,
            phone and birthday.
            user (User): The User object that is currently logged in and making this request. This is used to ensure
            that only contacts belonging to this user are updated by themselfs or an admin/superuser.

    :param contact_id: int: Specify the contact to update
    :param body: ContactModel: Pass the new contact information to the update_contact function
    :param user: User: Get the user id from the jwt token
    :param db: Session: Access the database

    :return: The updated contact if the contact was found, and none otherwise
    :doc-author: Trelent
    """

    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging
            to this user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Identify which contact to remove
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
