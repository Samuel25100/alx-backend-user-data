#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """handle Basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 encoded header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header,str):
            return None
        if "Basic " not in authorization_header:
            return None
        encode = authorization_header.split()[-1]
        return encode

    def decode_base64_authorization_header(self,
                                        base64_authorization_header: str) -> str:
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
                        decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        result = decoded_base64_authorization_header.split(':')
        return (result[0], result[1])
