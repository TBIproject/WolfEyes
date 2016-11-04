# # Project \WolfEyes

This project is meant to use two webcams and locate an object over some surface.

## # WolfEyes's Library

This project also provide some libraries allowing fast and easy use of webcams, which we used to quickly craft object's extraction algorithms. Now you can use it too !

### \How to use the library ?

First, you should import objects from the Camera module:

```python
# Import the library
from WolfEyes.Camera import *
```

Then you can instanciate and use a webcam right away:

```python
# Fetch a Webcam object and initialize it
camera = Camera(id = 0)
```

From there, you have some options in regards to how you can fetch frames from your webcam.

#### First way:

```python
while True:

  # Get the frame
  frame = camera.getFrame()

  # If frame is False: something went wrong
  if frame is not False:
    imshow('frame', frame)
    imshow('same frame', cam.frame)

  else: break
```

#### Second way:

```python
for frame in camera.flow:

  # Same shit, if anything go wrong, get out !
  if frame is not False:
    imshow('frame', frame)

  else: break
```

When you have finished with your camera(s), you can end it all:

```python
# Release every camera
Camera.releaseAll()

# Destroy all remaining cv2's imshow(...) windows
cv2.destroyAllWindows()
```
