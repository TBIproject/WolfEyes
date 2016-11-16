# # pyon object

Why ? Because python dict's syntax isn't always very comfy, while JSON's object data access is.
So instead of writing boring things and trying to see if anything already exist or not, pyon
comes in rescue for us, lazy developers...

## \Examples of use:

```python
# Let's import the guy
from WolfEyes.Utils import pyon

# Instanciation:
obj1 = pyon()
obj2 = pyon(key1 = value1, key2 = value2, ...)
obj3 = pyon({"key1": value1, "key2": value2, ...})

# Attribute assignement: (both equivalent)
obj1['attr'] = some_value...
obj1.attr = some_value...

# Attribute retreivement: (both equivalent)
temp = obj2['key2'] == obj2.key2
# temp = True

temp = obj1.missing_attribute
# temp = None

obj1.setUnknown('wtf is this?')
temp = obj1.missing_attribute
# temp = "wtf is this?"

# Random function with keyworded args:
def some_func(**kwargs): print(kwargs)

# This does works:
some_func(**ob3)
```
