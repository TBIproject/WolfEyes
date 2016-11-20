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
        this._POINTS = pyon()

    @property
    def position(this): return this._POSITION

    @property
    def points(this): return this._POINTS

    # Add a point to the point dict
    def setPoint(this, key, value):
        this._POINTS[key] = value

    def positionFromOIJ(this, **kargs):

        o = kargs.get('o', this._POINTS.o)
        i = kargs.get('i', this._POINTS.i)
        j = kargs.get('j', this._POINTS.j)

        #o, i, j = [(int(k * this.sourceHeight) if isinstance(k, float) else k) for k in (o, i, j)]
