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

    def __init__(this, *args, **kargs):
        """Constructor
        """

        Camera.CAMERA_SET.add(this)

        this.data = pyon()

        this.__ONFRAMEGET = lambda frame: frame

        this.__VIDCAP = None
        this.__LASTFRAME = None
        this.__LASTFRAME_AREA = None
        this.__LASTCONFIG = pyon()
        this.__FOV = D2Point()
        this.__AREA = pyon(
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

        if (not kargs.get('id', False) is False):
            this.init(0)

    ### INIT

    @property
    def videoCapture(this): return this.__VIDCAP

    @property
    def fov(this): return this.__FOV

    @property
    def area(this): return this.__AREA

    @property
    def baseFrame(this): return this.__LASTFRAME

    @property
    def frame(this): return this.__LASTFRAME_AREA

    @property
    def lastConfig(this): return this.__LASTCONFIG

    @property
    def baseHeight(this): return this.__LASTCONFIG.height

    @property
    def baseWidth(this): return this.__LASTCONFIG.width

    # Init and config camera
    def init(this, id, **kargs):
        """Capture and camera initialisation"""
        if this.__VIDCAP: this.release()
        this.__VIDCAP = cv2.VideoCapture(id)

        if not this.__VIDCAP.isOpened(): raise DeviceNotFoundException("Could not find device with id '%d'" % id)

        # Force 'high fps' if not defined
        kargs['fps'] = kargs.get('fps', 120.)

        this.config(**kargs)
        this.config(get=True)

        this.setArea(
            this.__AREA.topleft.x,
            this.__AREA.topleft.y,
            this.__AREA.bottomright.x,
            this.__AREA.bottomright.y,
            this.__AREA.skip.x,
            this.__AREA.skip.y
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
        if kargs.get('get', False) is True:
            for prop in Camera.props: result[prop] = this.getProp(prop)

        else: # Assign each value to paired prop passed in kargs
            for param, value in kargs.items(): this.setProp(param, value)
            for param in kargs: result[param] = this.getProp(param)

        this.__LASTCONFIG.update(result)
        return result

    def isInit(this):
        """Is the device capturing ?"""
        return not not this.__VIDCAP

    def checkInit(this):
        """Crash if not capturing"""
        if not this.__VIDCAP:
            raise CameraNotInitializedException('Camera is not initialized')
        elif not this.__VIDCAP.isOpened():
            raise CameraNotInitializedException("Camera is not initialized correctly, maybe device was not found")

    def setArea(this, x, y, u, v, m, n):
        """Region of interest"""
        x, u = [(int(i * this.baseWidth) if type(i) == float else i) for i in (x, u)]
        y, v = [(int(i * this.baseHeight) if type(i) == float else i) for i in (y, v)]

        print(this.baseWidth, this.baseHeight)

        this.__AREA.topleft.x = x
        this.__AREA.topleft.y = y
        this.__AREA.skip.x = m

        this.__AREA.bottomright.x = u
        this.__AREA.bottomright.y = v
        this.__AREA.skip.y = n

    # Define custom image processing via decoration
    def onFrameGet(func):
        def processSaver(this):
            this.__ONFRAMEGET = func
        return processSaver

    def getFrame(this):
        """Get a frame from videoCapture object"""
        this.checkInit()

        ret, frame = this.__VIDCAP.read()
        if ret is True:
            this.__LASTFRAME = this.__ONFRAMEGET(frame)
            this.__LASTFRAME_AREA = frame[
                this.__AREA.topleft.x:this.__AREA.bottomright.x:this.__AREA.skip.x,
                this.__AREA.topleft.y:this.__AREA.bottomright.y:this.__AREA.skip.y,
                :
            ]
        return ret

    @property
    def flow(this, source=False):
        """for image in camera.flow: doThings()
        This provide constant image stream if available"""
        this.checkInit()

        while True:
            this.getFrame()
            yield this.__LASTFRAME if source else this.__LASTFRAME_AREA

    def getProp(this, prop):
        """Getting camera's property"""
        this.checkInit()
        return this.__VIDCAP.get(Camera.props.get(prop, prop))

    def setProp(this, prop, value):
        """Setting camera's property"""
        this.checkInit()
        this.__VIDCAP.set(Camera.props.get(prop, prop), value)

    def exposure(this): return this.getProp('exposure')
    def height(this): return this.getProp('height')
    def width(this): return this.getProp('width')
    def fps(this): return this.getProp('fps')

    def release(this):
        """Stop capturing"""
        if this.__VIDCAP: this.__VIDCAP.release()
        this.__VIDCAP = None

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
            print(camera)
            camera.release()

    # On coupe tout
    @staticmethod
    def closeCamApp():
        """Stop capturing and destroy cv2 windows in case"""
        Camera.releaseAll()
        cv2.destroyAllWindows()
