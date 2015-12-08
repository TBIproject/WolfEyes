"""
Tentative d'interface en console basé sur un système similaire aux winforms...
Juste pour tuer le temps.
C'est moche.
Berk.
"""
import shutil
import os

# Clear the screen
def cls(): os.system('cls' if os.name=='nt' else 'clear')
# Terminal size
def termSize(fallback=(80, 25)): shutil.get_terminal_size(fallback)

# Truc chelou
class Unique:
	def __init__(this, init=[]):
		this.__list = {}
		for control in init: this.add(control)
	def __getitem__(this, item):
		return this.__list[item]
	def __delitem__(this, item):
		this.remove(item)
	def __contains__(this, item):
		return item in this.__list
	def __len__(this):
		return len(this.__list)
	def __iter__(this):
		return this.__list.__iter__()
	def __add__(this, controls):
		result = Unique(this)
		for control in controls: result.add(control)
		return result
	def __repr__(this):
		return 'Unique%s' % str(list(this))
	
	def add(this, thing):
		this.__list[thing] = this.__list.get(thing, thing)
	def append(this, thing):
		this.add(thing)
	def remove(this, thing):
		if thing in this.__list: del this.__list[thing]
		
	@property
	def count(this):
		return len(this.__list)
###

# Composite
class Control:
	def __init__(this, name=""):
		this.name = name
		this.controls = Unique()
		this.autoFillHeight = Unique()
		this.autoFillWidth = Unique()
		this.parent = None
		this.height = 1
		this.width = 1
	
	def __repr__(this):
		return "Control['%s':%d]" % (this.name, this.controls.count)
	
	def add(this, control):
		if isinstance(control, Control):
			this.controls.add(control)
		else: raise Exception('Not a Control object')
	
	def remove(this, control):
		this.controls.remove(control)
	
	@property
	def children(this):
		current = Unique([this])
		for control in this.controls: current += control.children
		return current
	
	def autoSpace(this):
		return 0 # Fuck this shit
	
	def fillHeight(this):
		if not parent: height = termSize()
		else: height = parent.autoSpace()
		
		this.height = height
		return height
		
	def fillWidth(this):
		if not parent: width = termSize()
		else: width = parent.autoSpace()
		
		this.width = width
		return width