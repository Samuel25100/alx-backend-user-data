#!/usr/bin/env python3
"""_hash_password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """hash the password from user db"""
    pass_by = password.encode('utf-8')
    return bcrypt.hashpw(pass_by, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """constructor of Auth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user"""
        hashed_password = _hash_password(password)
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            nuser = self._db.add_user(email=email,
                                      hashed_password=hashed_password)
            return nuser
        if user:
            raise ValueError(f'User {email} already exists')
