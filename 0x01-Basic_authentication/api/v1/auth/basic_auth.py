#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth


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
