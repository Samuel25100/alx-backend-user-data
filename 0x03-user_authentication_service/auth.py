#!/usr/bin/env python3
"""_hash_password"""
import uuid
import bcrypt
import typing
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """hash the password from user db"""
    pass_by = password.encode('utf-8')
    return bcrypt.hashpw(pass_by, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid"""
    return str(uuid.uuid4())


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
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            nuser = self._db.add_user(email, hashed_password)
            return nuser

    def valid_login(self, email: str, password: str) -> bool:
        """validate give email and password is correct"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                pwd = password.encode('utf-8')
                return bcrypt.checkpw(pwd, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create session for user by email"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                return session_id
        except Exception:
            return None
