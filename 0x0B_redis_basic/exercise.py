#!/usr/bin/env python3
"""
This module contains a Cache class for interacting with Redis, specifically
for storing and retrieving data with generated keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional

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

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieves data from Redis and applies a conversion function if provided.

        Parameters
        ----------
        key : str
            The key to retrieve the data from Redis.
        fn : Callable, optional
            A function to apply to the data to convert it back to the desired format.

        Returns
        -------
        Optional[Union[str, bytes, int, float]]
            The retrieved data in its original format if the key exists, otherwise None.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis and converts it to a string.

        Parameters
        ----------
        key : str
            The key to retrieve the data from Redis.

        Returns
        -------
        Optional[str]
            The retrieved data as a string if the key exists, otherwise None.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis and converts it to an integer.

        Parameters
        ----------
        key : str
            The key to retrieve the data from Redis.

        Returns
        -------
        Optional[int]
            The retrieved data as an integer if the key exists, otherwise None.
        """
        return self.get(key, int)
