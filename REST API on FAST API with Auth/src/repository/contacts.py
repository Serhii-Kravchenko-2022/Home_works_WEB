from typing import List
from datetime import timedelta, date

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas import ContactModel


async def get_contacts(offset: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(offset).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def get_contacts_by_firstname(first_name: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.first_name.like(f'%{first_name}%')).all()


async def get_contacts_by_lastname(last_name: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.last_name.like(f'%{last_name}%'))).all()


async def get_contacts_by_email(email: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.email.like(f'%{email}%'))).all()


async def get_contacts_by_birthday(user: User, db: Session) -> List[Contact]:
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
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone,
                      birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
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
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
