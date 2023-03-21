from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.connect_db import get_db
from src.database.models import User
from src.shemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(offset: int = 0,
                       limit: int = 100,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.

    :param offset: int: Specify the number of records to skip
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database connection to the repository
    :param current_user: User: Get the current user
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(offset, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    If no such contact exists, it raises an HTTP 404 error.

    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/{first_name}", response_model=List[ContactResponse])
async def get_contacts_by_name(first_name: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts_by_name function returns a list of contacts that match the first name provided.
        The function takes in a string representing the first name and an optional database session object,
        which is used to access the database. If no db session is provided, then one will be created by
        calling get_db(). The current user can also be optionally passed into this function as well.

    :param first_name: str: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A list of contacts that match the first name provided
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_by_firstname(first_name, current_user, db)
    return contacts


@router.get("/{last_name}", response_model=List[ContactResponse])
async def get_contacts_by_lname(last_name: str, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts_by_lname function returns a list of contacts with the specified last name.
        The function takes in a string representing the last name and returns a list of contact objects.

    :param last_name: str: Specify the last name of the contact to be retrieved
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contacts that have the same last name
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_by_lastname(last_name, current_user, db)
    return contacts


@router.get("/{email}", response_model=List[ContactResponse])
async def get_contacts_by_email(email: str, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts_by_email function is used to retrieve a list of contacts from the database
        that have an email address matching the one provided in the request.

    :param email: str: Define the email of the contact we want to retrieve
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_by_email(email, current_user, db)
    return contacts


@router.get("//birthday", response_model=List[ContactResponse])
async def get_contact_by_birthday(db: Session = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_birthday function returns a contact by birthday.
        Args:
            db (Session, optional): [description]. Defaults to Depends(get_db).
            current_user (User, optional): [description]. Defaults to Depends(auth_service.get_current_user).

    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts_by_birthday(current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input and returns the newly created contact.

    :param body: ContactModel: Define the type of data that will be passed to the function
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user that is currently logged in
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactModel object containing the new values for the contact.
            - contact_id: An integer representing the ID of an existing contact to be updated.
            - db (optional): A Session object that can be used to access and modify data in a database, if needed.

    :param body: ContactModel: Pass the data from the request body to the function
    :param contact_id: int: Specify the contact that is to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
