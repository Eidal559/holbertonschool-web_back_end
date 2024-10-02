#!/usr/bin/env python3
import re

def filter_datum(fields, redaction, message, separator):
    for field in fields:
        # Use regex to search for the field and replace its value
        message = re.sub(rf'(?<={field}=)[^{separator}]+', redaction, message)
    return message
