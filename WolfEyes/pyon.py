# -*- coding: utf-8 -*-
"""Flexible json-like dict"""
import json

class pyon(dict):
	"""This class mimics the way JSON works in Javascript
	(almost)"""

	def __init__(this, init=None, unknown=None, *args, **kargs):
		this.__dict__['__pyon_unknown'] = unknown
		dict.__init__(this, *args, **kargs)
		if init: this.load(init)

	def setUnknown(this, value):
		this.__dict__['__pyon_unknown'] = value;

	def __getattr__(this, attr):
		return this.get(attr, this.__dict__['__pyon_unknown'])

	def __setattr__(this, attr, value):
		this[attr] = value
		return this[attr]

	def __delattr__(this, attr):
		del this[attr]

	def __missing__(this, attr):
		return this.__unknown

	def __str__(this): return json.dumps(this)
	def __repr__(this): return str(this)

	def copy(this):
		copy = pyon()
		return copy.load(this)

	def load(this, thing):
		this.clear()
		if isinstance(thing, str): this.update(json.loads(thing))
		else: this.update(thing)
		return this

	def writeFile(filename="./", mode="w"):
		pass

	def readFile(filename="./", mode="r"):
		pass
### PYON
