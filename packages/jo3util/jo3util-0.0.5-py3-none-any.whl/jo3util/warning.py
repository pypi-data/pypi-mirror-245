#! /usr/bin/env python3
# vim:fenc=utf-8

"""

"""

import warnings

class ToDoWarning(Warning):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return repr(self.message)

def todo(msg):
    warnings.warn(msg, ToDoWarning)
