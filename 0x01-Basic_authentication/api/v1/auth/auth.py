#!/usr/bin/env python3
"""authorization handler class"""


class Auth:
    """handle authorization for basic api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        return False

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
