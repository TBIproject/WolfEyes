from konsola import *

a = Control('a')
b = Control('b')
c = Control('c')
d = Control('d')

a.add(b)
a.add(c)
b.add(d)

print a.children