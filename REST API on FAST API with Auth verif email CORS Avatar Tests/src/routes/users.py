from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.connect_db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.shemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Get the current user
    :return: The current_user object, which is the authenticated user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            current_user (User): The currently logged in user.
            db (Session): A database session object for interacting with the database.

    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary.uploader.upload(file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill')
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
