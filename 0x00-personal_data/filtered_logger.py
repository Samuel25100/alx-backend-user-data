#!/usr/bin/env python3
"""function: filter_datum"""
import logging
import re

logging.basicConfig(level=logging.INFO)

def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    out = []
    for field in fields:
        pattern = r"{}=.*?{}".format(field, separator)
        message = re.sub(pattern, r"{}={}{}".format(field, redaction, separator),
                      message)
    return message
