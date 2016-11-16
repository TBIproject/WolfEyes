# # Project \WolfEyes

This project is meant to use two webcams and locate an object over some surface.

## # WolfEyes's Library

This project also provide some libraries allowing fast and easy use of webcams, which we used to quickly craft object's extraction algorithms. Now you can use it too !

- WolfEyes.Project:
  - [Camera object doc](WolfEyes/Markdown/Camera.md) (basic image acquisition)
  - [ProcessUnit object doc](WolfEyes/Markdown/ProcessUnit.md) (builtin image processing utilities)
  - [WolfEye object doc](WolfEyes/Markdown/WolfEye.md) (WolfEyes's specific ProcessUnit)

### \Package architecture
- **WolfEyes**
  - Sub-Package:
    - **Utils**
      - Modules:
        - **TypeChecker**: Custom made decorators for type checking (function arguments and return values)
        - **Filters**: Module with various image processing functions.
        - **Tools**: Module with various tools in general.
      - Objects:
        - **D2Point**: 2D-Vector-like object
        - **pyon**: JSON-like object based on *dict* ([why?](WolfEyes/Markdown/pyon.md))
  - Objects:
    - **Camera**: Image acquisition object
    - **ProcessUnit**: Image processing object
    - **WolfEyes**: Project object

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
