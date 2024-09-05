#!/usr/bin/env python3
"""authorization handler class"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """handle authorization for basic api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path == "/api/v1/status" and "/api/v1/status/" in excluded_paths:
            return False
        if (path == "/api/v1/auth_session/login" and 
            "/api/v1/auth_session/login/" in excluded_paths):
            return False
        pa = ['/status', '/stats/', '/unauthorized/', '/forbidden/', '/users/']
        for i in excluded_paths:
            if '*' in i:
                expand = i.split('*')[0].split('/')[-1]
                for j in pa:
                    if expand in j:
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorized header 'Authorization' from request"""
        if request is None:
            return None
        auth = request.headers.get('Authorization')
        if not (auth):
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """will be overload by basic_auth"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        session_n = getenv('SESSION_NAME')
        return request.cookies.get(session_n)
