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

IntentName = str
Intent = namedtuple('Intent', ['name'])
