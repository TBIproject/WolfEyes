#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from WolfEyes.WolfEye import *

cam = ProcessUnit(id = 0)
cam.setArea(
    (0, .45),
    (1., .55)
)

@cam.onFrameGet
def test(frame):
    cam.process()

@cam.addProcess
def proc1(frame):
    frame[::, ::3] = (0, 0, 255)

# Actual loop
for frame in cam.flow:

    cv2.imshow('test', cam.processedFrame)
    cv2.imshow('src', cam.source)

    key = cv2.waitKey(1) & 0xFF
    if chr(key).lower() == 'q': break

Camera.closeCamApp()
