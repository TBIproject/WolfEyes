# -*- coding: utf-8 -*-
"""Custom weird vector, very useful."""
import math

# Plus simple pour gérer les points/vecteurs 2d
class D2Point(object):
	"""Some custom vector"""
	
	# Valeur d'arrondi extrême
	ROUND = 14
	
	# Init
	def __init__(this, x=0, y=0):
		this.x = x
		this.y = y
	
	# Getters/Setters
	
	@property
	def x(this): return round(this.__X, this.ROUND)
	
	@property
	def y(this): return round(this.__Y, this.ROUND)
	
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
	
	# Puissance
	def __pow__(this, r):
		if isinstance(r, D2Point): return D2Point(this.x ** r.x, this.y ** r.y)
		else: return D2Point(this.x ** r, this.y ** r)
	
	# Opposé
	def __neg__(this): return D2Point(-this.x, -this.y)
	
	# Clone (+D2Point)
	def __pos__(this):
		"""'+this' : clones itself"""
		return D2Point(this.x, this.y)
		
	def clone(this):
		"""Returns a new vector with same coords as current"""
		return +this
	
	# Module/Taille
	def __abs__(this): return math.sqrt(this.x**2 + this.y**2)
	def __len__(this): return abs(this)
	
	# Taille du vecteur
	@property
	def length(this): return abs(this)
	@length.setter
	def length(this, m):
		size = this.length
		if size: # Si le vecteur n'est pas nul
			this.x *= float(m) / size
			this.y *= float(m) / size
		return this
	
	# Partie entière
	@property
	def int(this):
		"""Returns new vector as current with integer coordinates"""
		return D2Point(int(this.x), int(this.y))
	
	# Conversion en tuple (~D2Point)
	def __invert__(this): return (this.x, this.y)
	def tuple(this):
		"""Returns current as a tuple"""
		return ~this
		
	# Modulation/moyenne (a % b)
	def __mod__(this, m):
		if isinstance(m, D2Point): return (this + m) / 2.0
		else: # Si c'est un réel
			new = +this
			new.length = m
			return new
	
	# Vecteur unitaire
	@property
	def unit(this):
		"""Returns unitary vector from current"""
		return this % 1
	
	# Pente/Direction
	@property
	def slope(this):
		"""Gets vector slope from direction"""
		try: return this.y / this.x
		except: return None
	
	# Direction (angle)
	@property
	def direction(this):
		"""Gets current vector direction (radians)"""
		return math.atan(this.slope)
	
	# Changement de direction
	@direction.setter
	def direction(this, rad):
		"""Sets the current vector direction to 'rad' (radians)"""
		length = this.length
		dir = D2Point.createUnit(rad)
		this.x = dir.x * length
		this.y = dir.y * length
	
	# Easy Degrees
	@property
	def directionDeg(this):
		"""Gets current vector direction (degrees)"""
		return math.degrees(this.direction)
	
	# Création de vecteurs unitaires
	@staticmethod
	def createUnit(rad=0):
		"""Static method returning some unit vector from a given direction 'rad' (radians)"""
		return D2Point(math.cos(rad), math.sin(rad))
		
	# Easy Degrees
	@staticmethod
	def createUnitDeg(deg=0):
		"""Static method returning some unit vector from a given direction 'deg' (degrees)"""
		return D2Point.createUnit(math.radians(deg))
	
	# Rotation du vecteur
	def rotate(this, rad):
		"""Returns a new vector being the current rotated by 'rad' (radians)"""
		z = complex(this.x, this.y)
		u = D2Point.createUnit(rad)
		c = complex(u.x, u.y)
		new = z * c
		return D2Point(new.real, new.imag)
	
	# Easy Degrees
	def rotateDeg(this, deg):
		"""Returns a new vector being the current rotated by 'deg' (degrees)"""
		return this.rotate(math.radians(deg))
	
	# Réaction à "not this"
	def __nonzero__(this): return True