#!/usr/bin/env python3
"""basic auth"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from flask import request


class BasicAuth(Auth):
    """handle Basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 encoded header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if "Basic " not in authorization_header:
            return None
        encode = authorization_header.split()[-1]
        return encode

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode base64 encoded authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_by = base64.b64decode(base64_authorization_header)
            result = decoded_by.decode("utf-8")
            return result
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        result = decoded_base64_authorization_header.split(':')
        return (result[0], result[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        user = User()
        lsuser = user.search({'email': user_email})
        if not lsuser:
            return None
        for i in lsuser:
            if i.is_valid_password(user_pwd):
                return i
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        auth = self.authorization_header(request)
        encode = self.extract_base64_authorization_header(auth)
        decode = self.decode_base64_authorization_header(encode)
        user_cr = self.extract_user_credentials(decode)
        return self.user_object_from_credentials(user_cr[0], user_cr[1])
