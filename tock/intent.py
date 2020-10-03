# -*- coding: utf-8 -*-
"""
    The ``intent`` module
    ======================

    Use it to import very intent kinds.

    :Example:

    >>> from tock.intent import Intent
    >>> Intent(name = "greetings")
    Intent(name='greetings')

"""
from collections import namedtuple

Intent = namedtuple('Intent', ['name'])
# @dataclass
# class Intent:
#     def __init__(self, name: str):
#         self.__name = name
#
#     @property
#     def name(self) -> str:
#         parts = self.__name.split(":")
#         if len(parts) == 1:
#             return parts[0]
#         elif len(parts) >= 2:
#             return parts[1]
#         return ""
#
#     @property
#     def namespace(self) -> str:
#         parts = self.__name.split(":")
#         if len(parts) == 1:
#             return ""
#         elif len(parts) >= 2:
#             return parts[0]
#         return ""
