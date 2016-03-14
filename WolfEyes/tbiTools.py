# -*- coding: utf-8 -*-*
"""Tools for everyday tasks"""
from threading import Thread
from D2Point import *
from pyon import pyon
import Tkinter as Tk
import numpy as np
import cv2
import sys

# PRINTF!!
def printf(txt):
	"""No line feed at the end ! :D"""
	sys.stdout.write(txt)

# Dimensions d'une matrice (image)
def height(img):
	"""Get an image's height"""
	return np.shape(img)[0]
	
def width(img):
	"""Get an image's width"""
	return np.shape(img)[1]
	
def channels(img):
	"""List an image's channels"""
	shape = np.shape(img)
	return shape[2] if len(shape) > 2 else 1

# Constrain
def constrain(n, min, max): return min if n < min else max if n > max else n
def Constrain(min, max, *args):
	"""Constrain a value between min and max
	 syntax: constrain(min, max, value1, value2, value3, ...)
	         constrain(min, max, *arglist)"""
	result = []
	for n in args: result.append(constrain(n, min, max))
	return tuple(result)
	
# Image vide (easypeasy)
def Empty(**kargs):
	"""Creates an empty image from some inputs:
	 - channels: number of channels (3)
	 - height (1)
	 - width (1)"""
	channels = kargs.get('channels', 3)
	height = kargs.get('height', 1)
	width = kargs.get('width', 1)
	return np.zeros((height, width, channels), np.uint8) if channels > 1 else np.zeros((height, width), np.uint8)
	
# Image vide depuis une autre image
def EmptyFrom(img, chan=None):
	"""Creates an empty image from another (same size, uint8)"""
	if not chan: chan = channels(img)
	return Empty(height=height(img), width=width(img), channels=chan)
	
# Retourne la liste des maximums d'un contour
def limiter(contour, maxDist=0):
	"""Returns every extrem-bottom points from a contour"""
	cnt = contour.copy()
	initial = start = end = None
	
	for _ in xrange(len(cnt)):
		i = cnt[:,:,1].argmax()
		point = D2Point(cnt[i][0][0], cnt[i][0][1])
		
		# Si c'est le premier point
		if not initial:
			initial = start = end = point
		
		# Les suivants
		elif point.y >= (initial.y - maxDist):
		
			# Découpage
			if  point.x >= initial.x: end = point
			elif point.x < initial.x: start = point
		
		# Si on a fini
		else: break
		
		# On balade le point
		cnt[i][0] = [-1, -1]
	###
	
	# Résultat
	result = (start % end)
	result.y = initial.y
	
	return result

# _Anti _NOISE _Kernel
def anoisek(r=5, debug=False):
	"""Function to create a kernel for anti-noise purposes"""
	
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
	
	kernel /= kernel.sum()
	return kernel
###

# Retourne l'histogramme de l'image
def imhist(img, i=0):
	return cv2.calcHist([img], [i], None, [256], [0, 256])[:,0]
###

def histMean(hist):
	m = 0.0;
	for i in xrange(len(hist)): m += i * hist[i]
	return m / hist.sum()
###

def imEntropy(img):
	sum = img.shape[0] * img.shape[1]
	
	result = 0.0
	for i in xrange(3):
		chist = imhist(img, i)
		e = 0.0
		for j in xrange(len(chist)):
			p = chist[j] / sum
			e += p * (math.log(p, 2) if p else 0)
		result -= e
	return result / 3.0
###

def imEntropy2(img):
	sum = img.shape[0] * img.shape[1]

	result = 0.0
	for i in xrange(3):
		chist = imhist(img, i)
		
		p = chist / sum
		e = (p * np.log2(p)).sum()
		
		result -= e
	
	return e / 3.0
###

# Création d'une image à partir d'un histogramme
def histogram(img, gamma=0.3):
	"""Creates an image's histogram to display"""
	
	shape = img.shape
	cans = shape[2] if len(shape) > 2 else 1
	result = np.zeros((256, 256, cans), np.uint8)
	max = height(img) * width(img)
	
	# Si l'image possède plusieurs cannaux
	for i in range(cans):
		
		# On calcule
		hist = imhist(img)
		values = (255 * (hist / max)**gamma).astype(np.uint8)
		
		# On affiche
		for j in xrange(len(values)):
			result[:values[j], j, i] = 255
	
	# RETURN
	return result

def coloroffset(img):
	min = img.min(axis=2)
	off = np.zeros(img.shape, img.dtype)
	if len(off.shape) > 2:
		for i in xrange(off.shape[2]): off[:,:,i] = min
	return off

# Essaye de supprimer le décalage absolu
def grounder(img, dtype=None):
	"""Tries to remove absolute offset
	'img' must be a 3 colors image"""
	shape = img.shape
	
	"""
	# Mise en forme
	a = img.reshape((shape[0] * shape[1], 3))
	min = np.zeros(a.shape)
	max = np.zeros(a.shape)
	
	# Minimas/maximas
	min[:,0] = min[:,1] = min[:,2] = a.min(axis=1)
	max[:,0] = max[:,1] = max[:,2] = a.max(axis=1)
	
	# Remise en forme
	min = min.reshape(shape)
	max = max.reshape(shape)
	
	# Remise au ras du sol
	grounded = img - min
	
	# return (grounded / max).astype(np.float32)
	return (grounded / 255.0).astype(np.float32)
	"""#"""
	
	min = coloroffset(img)
	grounded = img - min
	if dtype is not None:
		grounded = grouded.astype(dtype)
	
	return grounded

def rgbsum(img):
	return img.sum(axis=2)
	
def crash(img, ksize=(5, 5), sigmaX=2, *args):
	mean = cv2.GaussianBlur(img, ksize, sigmaX, *args)
	print [img.min(), mean.min()]
	return (img.astype(np.int16) - mean.min()).clip(0, 255).astype(np.uint8)
	
# Objet pour retourner des trucs
class Statos:
	"""Gets a flow of image and creates some stats"""
	
	# Init <3
	def __init__(this, **kargs):
		this.setcount(kargs.get('count', 10))
	
	def reset(this):
		this.DONE = False
		this.__i = 0
		this.__j = 0
		this._mean = None
		this._max = None
		this._var = None
	
	def setcount(this, value):
		this.reset() # 16777216 = 2^32 / 256
		val = constrain(value, 0, 16777216)
		this.__meanCount = val
		this.__maxCount = val
		return this.__meanCount
	
	@property
	def meanCount(this): return this.__meanCount
	
	@meanCount.setter
	def meanCount(this, value): return this.setcount(value)
	
	@property
	def maxCount(this): return this.__maxCount
	
	@maxCount.setter
	def maxCount(this, value): this.__maxCount = value
		
	@property
	def i(this): return this.__i
	@property
	def j(this): return this.__j
	
	@property
	def mean(this):
		if this._mean is not None:
			return (this._mean / this.i).astype(np.uint8)
		else: return None
	
	# Miam
	def feed(this, img):
		if this._mean is None:
			this._mean = np.zeros(img.shape, np.uint32)
		if this._max is None:
			this._max = np.zeros(img.shape, np.uint8)
		if this._var is None:
			this._var = np.zeros(img.shape, np.uint8)
		
		if this.i < this.meanCount:
			this._mean += img
			this.__i += 1
		elif this.j < this.maxCount:
			diff = cv2.absdiff(this.mean, img)
			this._max = np.maximum(this._max, diff)
			this.__j += 1
		else: this.DONE = True
		
		return this._max
### END STATOS

# Create fullscreen window with canvas
def FullscreenCanvas(*args, **kargs):
	root = Tk.Tk()
	
	root.bind('<q>', lambda e: root.withdraw())

	# make it cover the entire screen
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(1)
	root.geometry("%dx%d+0+0" % (w, h))

	canvas = Tk.Canvas(root, *args, **kargs)
	canvas.pack(fill=Tk.BOTH, expand=Tk.YES)

	Thread(target=root.mainloop).start()
	
	return pyon(
		canvas=canvas,
		window=root
	)
###

def getScreenSize():
	r = Tk.Tk()
	p = pyon(
		height=r.winfo_screenheight(),
		width=r.winfo_screenwidth()
	)
	r.destroy()
	return p
###