import pickle
from typing import Optional

import redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.database.connect_db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    redis_cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the pwd_context object to verify that the
        plain-text password matches the hashed one.

        :param self: Represent the instance of the class
        :param plain_password: Store the password that is entered by the user
        :param hashed_password: Compare the hashed password in the database with the plain text password entered by user
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
        The hash is generated using the pwd_context object, which is an instance of Flask-Bcrypt's Bcrypt class.

        :param self: Represent the instance of the class
        :param password: str: Pass in the password that is being hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
        Args:
        data (dict): A dictionary containing the claims to be encoded in the JWT.
        expires_delta (Optional[float]): An optional parameter specifying how long, in seconds,
        the access token should last before expiring. If not specified, it defaults to 15 minutes.

        :param self: Access the class attributes
        :param data: dict: Pass the data that will be encoded in the jwt
        :param expires_delta: Optional[float]: Set the expiration time for the access token
        :return: An encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
        Args:
        data (dict): A dictionary containing the user's id and username.
        expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.

        :param self: Represent the instance of the class
        :param data: dict: Store the user's id, username and email
        :param expires_delta: Optional[float]: Set the expiration time for the refresh token
        :return: An encoded refresh token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    def create_email_token(self, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a token.
        The token is encoded with the SECRET_KEY, which is stored in the .env file.
        The algorithm used to encode the token is also stored in the .env file.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data to be encoded
        :return: A token that is encoded with the secret key and algorithm
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=3)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes a refresh_token as an argument and returns the email of the user if it's valid.
        If not, it raises an HTTPException with status code 401 (UNAUTHORIZED) and detail 'Could not validate
        credentials'.


        :param self: Represent the instance of the class
        :param refresh_token: str: Pass in the refresh token that is being decoded
        :return: The email of the user who is trying to access a protected route
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
        protected endpoints. It takes a token as an argument and returns the user
        associated with that token. If no user is found, it raises an HTTPException.

        :param self: Refer to the current class instance
        :param token: str: Get the token from the request header
        :param db: Session: Pass the database session to the function
        :return: A user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # user = await repository_users.get_user_by_email(email, db)
        # if user is None:
        #     raise credentials_exception

        user = self.redis_cache.get(f'user:{email}')
        if user is None:
            print("USER POSTGRES")
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.redis_cache.set(f'user:{email}', pickle.dumps(user))
            self.redis_cache.expire(f'user:{email}', 900)
        else:
            print("USER CACHE")
            user = pickle.loads(user)
        return user

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
        It does this by decoding the JWT using our secret key, then checking to make sure that it has a scope
        of 'email_token'.
        If it does not have this scope, we raise an HTTPException with status code 401 (UNAUTHORIZED) and detail
        message INVALID_SCOPE.
        If there is no error in decoding the JWT, we return the email address associated with that token.

        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email address of the user who is trying to verify their account
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'email_token':
                email = payload["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_SCOPE)
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()
