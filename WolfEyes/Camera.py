# -*- coding: utf-8 -*-
"""
WOLFEYES'S FRAMEWORK
Python 3 / OpenCV 3

This file describe the Camera object, useful for acquiring image feed from a webcam.
"""

import cv2
import numpy as np

from .pyon import pyon
from .D2Point import D2Point

# Exception types
class CameraNotInitializedException(Exception): pass
class DeviceNotFoundException(Exception): pass

# Camera class
class Camera(object):
    """Class modeling a webcam
    """

    # Common param list
    props = {
        'exposure': cv2.CAP_PROP_EXPOSURE,
        'height': cv2.CAP_PROP_FRAME_HEIGHT,
        'width': cv2.CAP_PROP_FRAME_WIDTH,
        'fps': cv2.CAP_PROP_FPS,
    }

    # Managed cameras list
    CAMERA_SET = set()

    def __init__(this, id = None, **kargs):
        """Constructor
        """

        Camera.CAMERA_SET.add(this)

        this.data = pyon()

        this._ONFRAMEGET = lambda frame: frame

        this._VIDCAP = None
        this._LASTFRAME = None
        this._LASTFRAME_AREA = None
        this._LASTCONFIG = pyon()
        this._FOV = D2Point()
        this._AREA = pyon(
            topleft = pyon(
                y = 0,
                x = 0
            ),
            bottomright = pyon(
                x = 1.,
                y = 1.
            ),
            skip = pyon(
                x = 1,
                y = 1
            )
        )

        if id is not None:
            this.initialize(id, **kargs)

    ### INIT

    @property
    def videoCapture(this): return this._VIDCAP

    @property
    def fov(this): return this._FOV

    @property
    def area(this): return this._AREA

    @property
    def source(this): return this._LASTFRAME

    @property
    def frame(this): return this._LASTFRAME_AREA

    @property
    def lastConfig(this): return this._LASTCONFIG

    @property
    def sourceHeight(this): return this._LASTCONFIG.height

    @property
    def sourceWidth(this): return this._LASTCONFIG.width

    # Init and config camera
    def initialize(this, id, **kargs):
        """Capture and camera initialisation"""

        this._LASTCONFIG.clear()
        if this._VIDCAP: this.release()
        this._VIDCAP = cv2.VideoCapture(id)

        if not this._VIDCAP.isOpened(): raise DeviceNotFoundException("Could not find device with id '%d'" % id)

        # Force 'high fps' if not defined
        kargs['fps'] = kargs.get('fps', 120.)

        this.config(**kargs)
        this.config() # Store config data

        this.setArea(
            (this._AREA.topleft.x, this._AREA.topleft.y),
            (this._AREA.bottomright.x, this._AREA.bottomright.y),
            (this._AREA.skip.x, this._AREA.skip.y)
        )

    # Camera configuration
    def config(this, **kargs):
        """Camera's configuration:
         - exposure: value < 0, brigther towards 0
         - height: camera's capture height
         - width: camera's capture width
         - fps: camera's frenquency
        """
        this.checkInit()
        result = pyon()

        # Get current config
        if not kargs:
            for prop in Camera.props: result[prop] = this.getProp(prop)

        else: # Assign each value to paired prop passed in kargs
            for param, value in kargs.items(): this.setProp(param, value)
            for param in kargs: result[param] = this.getProp(param)

        this._LASTCONFIG.update(result)
        return result

    def isInit(this):
        """Is the device capturing ?"""
        return this._VIDCAP.isOpened() if this._VIDCAP else False

    def checkInit(this):
        """Crash if not capturing"""
        if not this._VIDCAP:
            raise CameraNotInitializedException('Camera is not initialized')
        elif not this._VIDCAP.isOpened():
            raise CameraNotInitializedException("Camera is not initialized correctly, maybe device was not found")

    def setArea(this, topLeft, bottomRight, skip = (1, 1)):
        """Region of interest
        """
        x, y = topLeft
        u, v = bottomRight
        m, n = skip

        if not (this.sourceWidth and this.sourceHeight):
            raise CameraNotInitializedException("No camera configuration, initialize it")

        x, u = [(int(i * this.sourceWidth) if isinstance(i, float) else i) for i in (x, u)]
        y, v = [(int(i * this.sourceHeight) if isinstance(i, float) else i) for i in (y, v)]

        this._AREA.topleft.x = x
        this._AREA.topleft.y = y
        this._AREA.skip.x = m

        this._AREA.bottomright.x = u
        this._AREA.bottomright.y = v
        this._AREA.skip.y = n

    # Define custom image processing via decoration
    def onFrameGet(this, func):
        this._ONFRAMEGET = func
        return func

    def getFrame(this):
        """Get a frame from videoCapture object"""
        this.checkInit()

        ret, frame = this._VIDCAP.read()
        if ret is True:

            this._LASTFRAME = frame

            area = frame[
                this._AREA.topleft.y:this._AREA.bottomright.y:this._AREA.skip.y,
                this._AREA.topleft.x:this._AREA.bottomright.x:this._AREA.skip.x,
                :
            ]

            this._LASTFRAME_AREA = area
            area = this._ONFRAMEGET(area)
            if area is not None:
                this._LASTFRAME_AREA = area

            return this._LASTFRAME_AREA

        return False

    @property
    def flow(this, source=False):
        """for image in camera.flow: doThings()
        This provide constant image stream if available"""
        this.checkInit()

        while True:
            if not this.isInit(): return
            else: this.getFrame()

            frame = this._LASTFRAME if source else this._LASTFRAME_AREA
            yield frame

    def getProp(this, prop):
        """Getting camera's property"""
        this.checkInit()
        return this._VIDCAP.get(Camera.props.get(prop, prop))

    def setProp(this, prop, value):
        """Setting camera's property"""
        this.checkInit()
        this._VIDCAP.set(Camera.props.get(prop, prop), value)

    def exposure(this): return this.getProp('exposure')
    def height(this): return this.getProp('height')
    def width(this): return this.getProp('width')
    def fps(this): return this.getProp('fps')

    def release(this):
        """Stop capturing"""
        if this._VIDCAP: this._VIDCAP.release()
        this._VIDCAP = None

    # Camera object destruction
    def __del__(this):
        """Destructor (del this)"""

        this.release()
        Camera.CAMERA_SET.remove(this)

    @staticmethod
    def getFrames():
        """Get frames from all cameras"""
        for cam in Camera.CAMERA_SET: cam.getFrame()

    @staticmethod
    def getFramesAsync():
        """Get frames from all cameras asynchronously"""
        threads = []
        for camera in Camera.CAMERA_SET:
            thread = Thread(target=camera.getFrame)
            threads.append(thread)
            thread.start()
        for thread in threads: thread.join()

    @staticmethod
    def releaseAll():
        """Stop evrything"""
        for camera in Camera.CAMERA_SET:
            camera.release()

    # On coupe tout
    @staticmethod
    def closeCamApp():
        """Stop capturing and destroy cv2 windows in case"""
        Camera.releaseAll()
        cv2.destroyAllWindows()
