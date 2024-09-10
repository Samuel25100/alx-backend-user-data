#!/usr/bin/env python3
"""class DB"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """add user to db"""
        session = self._session
        user = User(email, hashed_password)
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs):
        """find and user using given attribute value"""
        session = self._session
        if 'email' not in kwargs or len(kwargs) != 1:
            raise InvalidRequestError
        email = kwargs['email']
        user = session.query(User).filter_by(email=email).first()
        if user is None:
            raise NoResultFound
        return user
