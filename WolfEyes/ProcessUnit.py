# -*- coding: utf-8 -*-
"""
WOLFEYES'S FRAMEWORK
Python 3 / OpenCV 3

This file describe the ProcessUnit object, which is a camera with builtin image process tools.
"""

from .Camera import *

class ImageProcessingException(Exception): pass

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
    def clearProcessStack(): del this._PROCESS_STACK[:]

    # Generator applying a process and yielding the current state of the image
    def processByStep(this, **kargs):

        source = this._LASTFRAME_AREA if kargs.get('areaOnly', True) else this._LASTFRAME

        if source is not None:

            # We don't want to mess up the original image
            current = source.copy()
            for process in this._PROCESS_STACK:
                result = process.function(current, *process.args, **process.kargs)
                if result is not None: current = result
                this._PROCESSED_FRAME = current
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
    def addProcess(this, func = None, **kargs):

        def add(func):

            if not callable(func):
                raise TypeError("func should be a function, got %s instead" % type(func))

            this._PROCESS_STACK.append(pyon(
                function = func,
                args = kargs.get('args', ()),
                kargs = kargs.get('kargs', {})
            ))

            if kargs.get('verbose', False):
                print('added process:', func)
            return func

        return add(func) if func else add
