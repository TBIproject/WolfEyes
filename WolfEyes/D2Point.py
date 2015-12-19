# -*- coding: utf-8 -*-
from tbiTools import *
import math

# Plus simple pour gérer les points/vecteurs 2d
class D2Point(object):
	def __init__(this, x=0, y=0):
		this.x = x
		this.y = y
	
	# Getters/Setters
	
	@property
	def x(this): return this.__X
	
	@property
	def y(this): return this.__Y
	
	@x.setter
	def x(this, value):
		r = this.__X = float(value)
		return r
	
	@y.setter
	def y(this, value):
		r = this.__Y = float(value)
		return r
	
	# ToString
	def __str__(this):
		return '(%s, %s)[%s]' % (this.x, this.y, abs(this))
	def __repr__(this): return str(this)
	
	# Addition
	def __add__(this, p):
		if isinstance(p, D2Point): return D2Point(this.x + p.x, this.y + p.y)
		else: return D2Point(this.x + p, this.y + p)
	
	# Soustraction
	def __sub__(this, p):
		if isinstance(p, D2Point): return D2Point(this.x - p.x, this.y - p.y)
		else: return D2Point(this.x - p, this.y - p)
	
	# Division
	def __div__(this, r):
		if isinstance(r, D2Point): return D2Point(this.x / r.x, this.y / r.y)
		else: return D2Point(this.x / r, this.y / r)
	
	# Multiplication
	def __mul__(this, r):
		if isinstance(r, D2Point): return D2Point(this.x * r.x, this.y * r.y)
		else: return D2Point(this.x * r, this.y * r)
	
	# Opposé
	def __neg__(this): return D2Point(-this.x, -this.y)
	
	# Clone (+D2Point)
	def __pos__(this): return D2Point(this.x, this.y)
	
	# Module/Taille
	def __abs__(this): return math.sqrt(this.x**2 + this.y**2)
	def __len__(this): return abs(this)
	
	@property
	def length(this): return abs(this)
	@length.setter
	def length(this, m):
		size = this.length
		if size: # Si le vecteur n'est pas nul
			this.x *= float(m) / size
			this.y *= float(m) / size
		return this
	
	@property
	def int(this): return D2Point(int(this.x), int(this.y))
	
	# Conversion en tuple (~D2Point)
	def __invert__(this):
		return (this.x, this.y)
		
	# Modulation/moyenne (a % b)
	def __mod__(this, m):
		if isinstance(m, D2Point): return (this + m) / 2.0
		else: # Si c'est un réel
			new = D2Point(1, 1)
			new.length = m
			return new
	
	# Réaction à "not this"
	def __nonzero__(this): return True