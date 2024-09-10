#!/usr/bin/env python3
"""_hash_password"""
import bcrypt

def _hash_password(password):
    """hash the password from user db"""
    pass_by = password.encode('utf-8')
    return bcrypt.hashpw(pass_by, bcrypt.gensalt())
