#!/usr/bin/env python3

from typing import List, Tuple


def element_length(lst: List[str]) -> List[Tuple[str, int]]:
    """Returns a list of tuples containing each element of its length."""
    return [(i, len(i)) for i in lst]
