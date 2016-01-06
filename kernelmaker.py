import numpy as np
import math, sys

def printf(txt):
	sys.stdout.write(txt)
###

def anoisek(r=5, debug=False):
	"""Function to create a kernel for anti-noise purposes
	"""

	w, h = 2*r+1, 2*r+1
	kernel = np.zeros((w, h), np.float32)
	
	if debug: print
	for u in xrange(w):
		x = r - u
		
		for v in xrange(h):
			y = r - v
			
			dist = (x**2 + y**2) ** 0.5
			val = dist/r
			
			if dist <= r:
				kernel.itemset((u, v), val)
				if debug: printf('#')
			elif debug: printf(' ')
		###
		if debug: printf('\n ')
	###
	
	return kernel
###

anoisek(10, True)
raw_input()