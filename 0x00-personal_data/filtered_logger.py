#!/usr/bin/env python3
"""function: filter_datum"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        pattern = r"{}=.*?{}".format(field, separator)
        message = re.sub(pattern, r"{}={}{}".format(field, redaction,
                                                    separator), message)
    return message
