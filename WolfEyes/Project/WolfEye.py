# -*- coding: utf-8 -*-
"""
WOLFEYES'S FRAMEWORK
Python 3 / OpenCV 3

This file describe the WolfEye object, which is a Camera with some extra data.
"""

from .ProcessUnit import *

class WolfEye(ProcessUnit):

    def __init__(this, id = None, **kargs):
        super().__init__(id, **kargs)

        this._POSITION = None

    @property
    def position(this): return this._POSITION
