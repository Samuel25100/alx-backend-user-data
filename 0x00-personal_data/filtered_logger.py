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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor of RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """return formated and obfuscated message"""
        message = super(RedactingFormatter, self).format(record)
        result = filter_datum(self.fields, self.REDACTION,
                              message, self.SEPARATOR)
        return (result)
