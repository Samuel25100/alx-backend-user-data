#!/usr/bin/env python3
"""Session authentication expiration"""
import datetime
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """handle expiration of session"""

    def __init__(self):
        """constructor for session att"""
        self.session_duration: int = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """overload create_session of SessionAuth"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = user_id
        self.user_id_by_session_id['created_at'] = datetime.datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overload user_id_for_session_id of SessionAuth"""
        if session_id is None:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        if 'created_at' not in self.user_id_by_session_id:
            return None
        dur = self.user_id_by_session_id['created_at']
        dur += datetime.timedelta(seconds=self.session_duration)
        now = datetime.datetime.now()
        if dur < now:
            return None
        else:
            return user_id
