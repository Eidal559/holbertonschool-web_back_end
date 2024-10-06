#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, Optional, TypeVar


class Auth:
    """ Auth Class """

    def __init__(self):
        """Constructor"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): List of paths that do not require
            authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path consistency by removing trailing slashes for comparison
        path = path.rstrip('/')

        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths.rstrip('*')):
                    return False
            elif path == paths.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            Optional[str]: The Authorization header or None if not present.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(
        self, request=None
    ) -> Optional[TypeVar('User')]:  # type: ignore
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            Optional[TypeVar('User')]: The current user or None.
        """
        return request  # Placeholder for actual implementation
