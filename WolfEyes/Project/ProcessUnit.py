# -*- coding: utf-8 -*-
"""
WOLFEYES'S FRAMEWORK
Python 3 / OpenCV 3

This file describe the ProcessUnit object, which is a camera with builtin image process tools.
"""

from .Camera import *
from ..Utils import TypeChecker

class ImageProcessingException(Exception): pass

# The function enrichissment object
class Process(object):

    def __init__(this, function, *args, **kargs):
        if not callable(function):
            raise TypeError("First argument should be callable, got %s" % type(function))

        this.owner = None
        this.function = function
        this.setArgs(*args, **kargs)

    def setOwner(this, owner):

        this.owner = owner

    def __call__(this, frame, *args, **kargs):

        owner = this.owner
        pargs = args or this.args
        pkargs = kargs or this.kargs

        if owner is None:
            return this.function(frame, *pargs, **pkargs)
        else:
            return this.function(owner, frame, *pargs, **pkargs)

    def setArgs(this, *args, **kargs):

        this.kargs = kargs
        this.args = args

    def __repr__(this): return "<Process over %s>" % this.function

# The webcam based object
class ProcessUnit(Camera):

    def __init__(this, id = None, **kargs):
        super().__init__(id, **kargs)

        this._PROCESS_STACK = []
        this._PROCESSED_FRAME = None

    @property
    def processedFrame(this): return this._PROCESSED_FRAME

    @property
    def processStack(this): return this._PROCESS_STACK

    # Clear the process stack
    def clearProcessStack(this): del this._PROCESS_STACK[:]

    # Moves processes to a certain index
    def moveProcess(this, index, *indexes):
        stack = this._PROCESS_STACK

        for i in indexes:
            stack.insert(index, stack.pop(i))
            index += 1

    # Generator applying a process and yielding the current state of the image
    def processByStep(this, **kargs):

        source = this._LASTFRAME_AREA if kargs.get('areaOnly', True) else this._LASTFRAME
        pyon = kargs.get('pyon', False)

        if source is not None:

            # We don't want to mess up the original image
            current = source.copy()
            this._PROCESSED_FRAME = source

            for process in this._PROCESS_STACK:
                result = process(current)

                if result is not None: current = result
                this._PROCESSED_FRAME = current

                if pyon:
                    yield pyon(
                        process = process,
                        frame = current
                    )
                else:
                    yield current

        else:
            # If there is no image to process, why bothering ?
            raise ImageProcessingException("There is no image in the buffer, can't process")

    # Process in one go
    def process(this, **kargs):

        # Apply each step
        for _ in this.processByStep(**kargs): pass

        # Final result
        return this._PROCESSED_FRAME

    # Decorator for adding processes to the stack
    @TypeChecker.args(index = int, replace = bool, own = bool)
    def addProcess(this, function = None, **kargs):

        index = kargs.get('index', len(this._PROCESS_STACK))
        replace = kargs.get('replace', False)
        own = kargs.get('own', False)

        def add(function, owner = None):

            if not callable(function):
                raise TypeError("Function should be callable, got %s" % type(function))

            # Create the rich function
            process = Process(function,
                *kargs.get('args', ()),
                **kargs.get('kargs', {})
            )

            # Pass the reference to current cam
            if own: process.setOwner(this)

            if replace:
                this._PROCESS_STACK.pop(index)
            this._PROCESS_STACK.insert(index, process)

            if kargs.get('verbose', False):
                print('added process:', function)
            return function

        return add(function) if function else add

    # Decorator for adding processes to the stack with owner awareness
    def addAwareProcess(this, function = None, **kargs):
        kargs['own'] = True
        return this.addProcess(function, **kargs)
