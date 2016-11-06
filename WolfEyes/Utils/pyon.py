# -*- coding: utf-8 -*-
"""Flexible json-like dict"""
import json

class CustomEncoder(json.JSONEncoder):
    def default(this, obj):
        try:
            return json.JSONEncoder.default(this, obj)
        except: pass
### CUSTOM ENCODER

class pyon(dict):
    """This class mimics the way JSON works in Javascript
    (almost)"""

    def __init__(this, init=None, *args, **kargs):
        """Dict derivation"""
        super().__init__(this, *args, **kargs)
        if init is not None: this.load(init)
        this.setUnknown(None)

    def setUnknown(this, value):
        this.__dict__['__pyon_unknown'] = value;
        return this

    def getUnknown(this):
        return this.__dict__['__pyon_unknown']

    # Easy storage of functions into pyon object
    def registerDecorator(this, key):
        def decorator(func):
            this[key] = func
            return func
        return decorator

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

    def __str__(this): return json.dumps(this, cls=CustomEncoder)
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

            json.dump(write, f, cls=CustomEncoder)

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
