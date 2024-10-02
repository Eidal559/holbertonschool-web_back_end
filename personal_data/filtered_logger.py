#!/usr/bin/env python3

import re

def filter_datum(fields, redaction, message, separator):
    pattern = '|'.join([rf'(?<={field}=)[^{separator}]+' for field in fields])
    return re.sub(pattern, redaction, message)
