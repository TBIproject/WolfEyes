#WIP
import json

class pyon(object):
	def __getattribute__(this, attr):
		if attr in pyon.__dict__:
			print 'ok'
			return this.__getattr__(attr)
		else: return this[attr] if attr in this else None
	
	def __setattr__(this, attr, value):
		this[attr] = value
		return this[attr]
	
	def __str__(this):
		return json.dumps(this)
	
	def load(this, json):
		this.clear()
		this.update(json.loads(json))
		return this
	
	def unify(this):
		return this.load(str(this))
### PYON