#!/usr/bin/env python3
"""authorization handler class"""
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
        else:
            return True

    def authorization_header(self, request=None) -> str:
        if request is None:
            return None
        auth = request.headers.get('Authorization')
        if not (auth):
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        return None
