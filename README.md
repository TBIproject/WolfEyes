# # Project \WolfEyes

This project is meant to use two webcams and locate an object over some surface.

## # WolfEyes's Library

This project also provide some libraries allowing fast and easy use of webcams, which we used to quickly craft object's extraction algorithms. Now you can use it too !

### \Package architecture
- **WolfEyes**
  - Sub-Packages:
    - **[Project](WolfEyes/Project)**:
      - Objects:
        - **[Camera](WolfEyes/Markdown/Camera.md)**: Basic image acquisition object
        - **[ProcessUnit](WolfEyes/Markdown/ProcessUnit.md)**: Image processing object
        - **[WolfEyes](WolfEyes/Markdown/WolfEyes.md)**: Project specific webcam object
    - **[Utils](WolfEyes/Utils)**
      - Modules:
        - **[TypeChecker](WolfEyes/Markdown/TypeChecker.md)**: Custom made decorators for type checking
        - **[Filters](WolfEyes/Markdown/Filters.md)**: Module with various image processing functions.
        - **[Tools](WolfEyes/Markdown/Tools.md)**: Module with various tools in general.
      - Objects:
        - **[D2Point](WolfEyes/Markdown/D2Point.md)**: 2D-Vector-like object
        - **[pyon](WolfEyes/Markdown/pyon.md)**: JSON-like object based on *dict* ([why?](WolfEyes/Markdown/pyon.md))

### \How to use the library ?

You can either import the whole package:

```python
# Import everything from the whole package:
from WolfEyes import *
```

Or you can import whatever you need precisely from the package:

```python
# Import what you want:
from WolfEyes.Project import Camera, ProcessUnit, WolfEye
from WolfEyes.Utils import TypeChecker, Tools, Filters, D2Point, pyon

# Or just everything:
from WolfEyes.Project import *
from WolfEyes.Utils import *
```
