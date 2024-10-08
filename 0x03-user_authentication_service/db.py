#!/usr/bin/env python3
"""class DB"""
from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import logging


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str,
                 hashed_password: str) -> User:
        """add user to db"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """find and user using given attribute value"""
        attribute = ['email', 'id', 'hashed_password', 'session_id', 'reset_token']
        inp = list(kwargs.keys())
        result = all(i in attribute for i in inp)
        if result is False or len(kwargs) != 1:
            raise InvalidRequestError
        use = self._session.query(User).all()
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update a specific user attribute value"""
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if not hasattr(user, key) or key == 'id':
                raise ValueError
            setattr(user, key, val)
        self._session.commit()
        return None
