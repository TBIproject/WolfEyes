# -*- coding: utf-8 -*-
"""Flexible json-like dict"""
import json

class pyon(dict):
    """This class mimics the way JSON works in Javascript
    (almost)"""

    def __init__(this, init=None, unknown=None, *args, **kargs):
        """Dict derivation
        init: Initial data (str or dict)
        unknown: Unknown value to use
        """
        dict.__init__(this, *args, **kargs)
        this.setUnknown(unknown)
        if init: this.load(init)

    def setUnknown(this, value):
        this.__dict__['__pyon_unknown'] = value;

    def getUnknown(this):
        return this.__dict__['__pyon_unknown']

    def __getattr__(this, attr):
        """When: this.attr
        """
        return this.get(attr, this.getUnknown())

    def __setattr__(this, attr, value):
        """When: this.attr = value
        """
        this[attr] = value
        return this[attr]

    def __delattr__(this, attr):
        """When: del this.attr
        """
        del this[attr]

    def __missing__(this, attr):
        """Return this['missing_key']
        """
        return this.getUnknown()

    def __str__(this): return json.dumps(this)
    def __repr__(this): return str(this)

    def copy(this):
        """Return a copy of this
        """
        return pyon(this)

    def load(this, thing, clear=True):
        """Load data to this.
        if thing is a string, guess its json as str
        else, guess its something dict.update valid
        if clear, then clear this before load
        """
        if clear: this.clear()
        if isinstance(thing, str): this.update(json.loads(thing))
        else: this.update(thing)
        return this

    def writeFile(this, filename, mode='w'):
        """Mode list:
         - 'w': replace everything
         - 'a': merge the data with old
        """
        with fopen(filename) as f:

            if mode is 'w':
                write = this

            elif mode is 'a':
                write = pyon().readFile(filename)
                write.update(this)

            else:
                raise Exception("mode is not in ['w', 'a']")

            json.dump(write, f)

    def loadFile(this, filename, mode='r'):
        """Mode list:
         - 'r': everything is replaced
         - 'a': merge the data with new
        """
        with fopen(filename, 'r') as f:

            if mode is 'r':
                clear = True

            elif mode is 'a':
                clear = False

            else:
                raise Exception("mode is not in ['r', 'a']")

            this.update(json.load(f), clear)
### PYON
