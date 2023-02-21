from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: date = Field()


# class ContactModel(ContactBase):
#     pass
#
# class ContactUpdate(ContactModel):
#     pass


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
