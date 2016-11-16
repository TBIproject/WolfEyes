# # ProcessUnit object

- **Parent**: [Camera object](Camera.md)

Getting frames from a webcam is quite easy. Now what if why were to process each image ?
This is where a ProcessUnit object becomes handy: It provides you with some kind of process
pipeline.

```python
# Let's import everything we need to manipulate a ProcessUnit
from WolfEyes.Project.ProcessUnit import *
import cv2

# Initialize the webcam
cam = ProcessUnit(id = 0)


# [...EXTRA...]

# Acquisition loop
for frame in cam.flow:

  if frame is False: break

  # Tell the camera object to apply its process
  processedFrame = cam.process()

  cv2.imshow('processedFrame', processedFrame)
  cv2.imshow('frame', frame)

# END FOR
```

So, this looks similar to the Camera object frame acquisition, but enables you to also process
each frame with custom functions. But what about them ? I can't see any in the previous example...

Well, if no function is defined, the processed image will simply be the source image.

But let us define some processing functions:

```python
# [EXTRA = ]

@cam.addProcess
def firstProcess(frame):
  frame[:, ::2, :] = (0, 0, 255)
#END FUNCTION

@cam.addProcess
def secondProcess(frame):
  new = frame.copy()
  new[::2, :, :] = (255, 0, 0)
  return new
#END FUNCTION
```

Now, for every frame, each function will be applied once, in the order of definition.
This is because the **@ProcessUnit.addProcess** decorator actually add the function passed
into the ProcessUnit's process stack. It is actually a plain list:

```python
cam.processStack
# [<function 'firstProcess' at 0x...>, <function 'secondProcess' at 0x...>]
```

Now, each processing function should take 1 argument: the current frame in the process (Because
  each process result is passed to the next processing function).

If you don't return anything, the current image reference will be kept, understand that it will
not be replaced, so in order for your processings to take effect, you will have to directly modify
the input image.

But if it ever happens that you need to use some second image for your transformations, and you would
like to use the new image as the current image to process, you can return it, and it will be
injected in the process line.

It may sound complicated, but it is really not:
- **No return**: Same image reference kept for further processing
- **Some return**: New returned reference kept for further processing
