# -*- coding: utf-8 -*-
"""
WOLFEYES'S FRAMEWORK
Python 3 / OpenCV 3

This file describe the ProcessUnit object, which is a camera with builtin image process tools.
"""

from .Camera import *
from .Utils import TypeChecker

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
            for process in this._PROCESS_STACK:
                result = process.function(current, *process.args, **process.kargs)
                if result is not None: current = result
                this._PROCESSED_FRAME = current

                if pyon:
                    pyonReturn = process.copy()
                    pyonReturn.update({'frame': current})
                    yield pyonReturn
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
    @TypeChecker.args(index = int, replace = bool)
    def addProcess(this, func = None, **kargs):

        index = kargs.get('index', len(this._PROCESS_STACK))
        replace = kargs.get('replace', False)

        def add(func):

            if not callable(func):
                raise TypeError("func should be callable, got %s" % type(func))

            process = pyon(
                function = func,
                args = kargs.get('args', ()),
                kargs = kargs.get('kargs', {})
            )

            if replace:
                this._PROCESS_STACK.pop(index)
            this._PROCESS_STACK.insert(index, process)

            if kargs.get('verbose', False):
                print('added process:', func)
            return func

        return add(func) if func else add
