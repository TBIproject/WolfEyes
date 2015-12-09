# -*- coding: utf-8 -*-
from tbiTools import *
import math

# Plus simple pour gérer les points/vecteurs 2d
class D2Point():
	def __init__(this, x=0, y=0):
		this.x = float(x)
		this.y = float(y)
	
	# ToString
	def __str__(this):
		return '(%s, %s)[%s]' % (this.x, this.y, abs(this))
	
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
	def length(this, val): return this % val
	
	@property
	def pos(this): return (this.x, this.y)
	
	# Vecteur unitaire (~D2Point)
	def __invert__(this):
		size = abs(this)
		u = 0 if not this.x else this.x / size
		v = 0 if not this.y else this.y / size
		return D2Point(u, v)
		
	# Modulation/moyenne (a % b)
	def __mod__(this, m):
		if isinstance(m, D2Point): return (this + m) / 2.0
		else: return (~this)*m
	
	# Réaction à "not this"
	def __nonzero__(this): return True