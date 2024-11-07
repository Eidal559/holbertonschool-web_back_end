#!/usr/bin/env python3
"""
This module contains a Cache class for interacting with Redis, specifically
for storing and retrieving data with generated keys, with functionality to
track method calls and maintain a history of inputs and outputs.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Parameters
    ----------
    method : Callable
        The method to be wrapped and counted.

    Returns
    -------
    Callable
        The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create a Redis key using the method's qualified name
        key = f"{method.__qualname__}"
        # Increment the count for this key in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs for a method.

    Parameters
    ----------
    method : Callable
        The method to be wrapped with history tracking.

    Returns
    -------
    Callable
        The wrapped method with input/output history functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create Redis keys for input and output history
        key_m = method.__qualname__
        inputs_key = f"{key_m}:inputs"
        outputs_key = f"{key_m}:outputs"
        
        # Log inputs
        self._redis.rpush(inputs_key, str(args))
        # Call the original method and store its output
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))
        return result
    return wrapper


def replay(func: Callable):
    """
    Displays the history of calls for a particular function, including inputs and outputs.

    Parameters
    ----------
    func : Callable
        The function whose call history will be displayed.
    """
    r = redis.Redis()
    key_m = func.__qualname__
    inputs = r.lrange(f"{key_m}:inputs", 0, -1)
    outputs = r.lrange(f"{key_m}:outputs", 0, -1)
    
    call_count = len(inputs)
    times_str = "time" if call_count == 1 else "times"
    print(f"{key_m} was called {call_count} {times_str}:")
    
    for inp, out in zip(inputs, outputs):
        print(f"{key_m}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")


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

    @call_history
    @count_calls
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
