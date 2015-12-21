import __init__ as init
import sys

def printf(txt): sys.stdout.write(txt)

OUT = sys.stdout
NUL = open('nul', 'w')
print '\n' * 100, """
><><><><><><><><><><><><><><><><><><><><><><><><><><><><
><                                                    ><
><  This script only check the .py file's syntax and  ><
><  create the .pyc by importing it.                  ><
><                                                    ><
><><><><><><><><><><><><><><><><><><><><><><><><><><><><
"""
for lib in init.__all__:
	try:
		printf('%-30s' % ('Importing %s... ' % lib))
		sys.stdout = NUL
		exec('import %s' % lib)
		sys.stdout = OUT
		printf('OK\n\n')
	except Exception as e:
		sys.stdout = OUT
		printf('ERROR:\n  > %s\n\n' % e)
NUL.close()
print '#Done'

try: input()
except: pass