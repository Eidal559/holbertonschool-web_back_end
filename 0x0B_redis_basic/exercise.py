#!/usr/bin/env python3
"""
This module contains a Cache class for interacting with Redis, specifically
for storing and retrieving data with generated keys.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    A class used to represent a Cache system using Redis.

    Attributes
    ----------
    _redis : redis.Redis
        an instance of the Redis client
    """

    def __init__(self):
        """
        Initializes the Cache class.

        Creates a Redis client and flushes any existing data in the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis using a randomly generated key.

        Parameters
        ----------
        data : Union[str, bytes, int, float]
            The data to be stored in Redis. It can be a string, bytes, integer, or float.

        Returns
        -------
        str
            A unique key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
