# # Camera object

In order to get images from a webcam, WolfEyes provides you with a camera object, which you must import:

```python
# Import the Camera object from the package
from WolfEyes.Project import Camera
```

Then you would instanciate the object, with an id corresponding to the webcam index (quite magical where the list comes from... Retrieved from OpenCV)

```python
# Fetch a Webcam object and initialize it
camera = Camera(id = 0)
```

From there, you have some options in regards to how you can fetch frames from your webcam:

## First way:

The basic way we use to do this: with a standard *while* loop from which we get out on demand.

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

## Second way:

Some more *hipsteristic* way to do it, I find it more elegant and readable:

```python
for frame in camera.flow:

  # Same shit, if anything go wrong, get out !
  if frame is not False:
    imshow('frame', frame)

  else: break
```

## When you are done:

When you have finished your work with your camera(s), you can end it all:

```python
# Release every camera
Camera.releaseAll()

# Destroy all remaining cv2's imshow(...) windows
cv2.destroyAllWindows()
```
