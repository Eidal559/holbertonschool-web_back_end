#!/usr/bin/env python3
"""
Main file
"""

from user import User  # Assuming the class is defined in user.py

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))
