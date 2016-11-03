from WolfEyes.Camera import *

cam = Camera()
cam.init(0)

print(cam.area)

while 1:
    cam.getFrame()
    cv2.imshow('test', cam.frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

Camera.closeCamApp()
