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

    def get_user_from_session_id(self, session_id: str) -> User:
        """get the user using session_id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """delete session_id or set it to None"""
        user = self._db.find_user_by(id=user_id)
        user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """reset the token for user by email"""
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except Exception:
            raise ValueError
