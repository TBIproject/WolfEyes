# -*- coding: utf-8 -*-
"""
AUTHOR(S): POPOLO, 
REQUIRE PYTHON 2.7x
REQUIRE CV2 3.x
NOTE: ON MESURE LES ANGLES DE DROITE A GAUCHE!
NOTE: ON UTILISE LES ANGLES EN RADIANS!
ON NE DIT PAS 'CANARD'!
"""
import time # Owi
import math # OWI
import sys # YEAH
print sys.version # Utile
try: # On essaye d'importer cv2
	import cv2; v = cv2.__version__ # CV2 VERSION
	if v[0] != '3': print "OpenCV 3.x required, got %s..." % (v); exit()
	del v # tout propre
except: print 'OpenCV 3.x is required... Missing'; exit()
from threading import Thread
import numpy as np

# Popote perso
import CustomFilter as cf
from tbiTools import *
from D2Point import *
from pyon import *

# RIP
# Gestion du repère, en mesure d'angles relatifs
class Space(object):
	def __init__(this, o=0, i=0, j=0):
		this.o = float(o)
		this.i = float(i)
		this.j = float(j)

# """
# Easy cam
class Camera(object):
	"""Class helping with cameras and OpenCV (still brain fucked)
	"""
	
	# Liste des paramètres communs
	props = {
		'exposure': cv2.CAP_PROP_EXPOSURE,
		'height': cv2.CAP_PROP_FRAME_HEIGHT,
		'width': cv2.CAP_PROP_FRAME_WIDTH,
		'fps': cv2.CAP_PROP_FPS,
	}
	
	# Formats d'images courants
	formats = set([(320, 240), (320, 480), (640, 480), (800, 600), (800, 720), (1024, 720), (1280, 720), (1280, 1024), (1280, 1080), (1440, 900), (1920, 1080)])
	
	# Temporisation
	@staticmethod
	def waitKey(t=1):
		k = cv2.waitKey(t) & 0xFF
		return k
	
	# Default key management method
	@staticmethod
	def defaultKeyManagement(k, cam):
		if k == 'q': return True # Stop
		
		elif k == 'o':
			cam.space.o = cam.finger.x
				
		elif k == 'i':
			cam.space.i = cam.finger.x
		
		elif k == 'j':
			cam.space.j = cam.finger.x
			
		elif k == ' ':
			cam.setReference(count=10)
			
		elif k == 'c':
			size = getScreenSize()
			cam.calibrate(True, w=size.width, h=size.height)
			
		elif k == '.':
			cam.Export('cam')
		
		elif k == '0':
			cam.Import('cam')
	###
	
	# On assigne la fonction de key management
	keyManagement = defaultKeyManagement
	
	# Celui qui fait tout
	@staticmethod
	def keyEvents(*args):
		k = Camera.waitKey(*args)
		if k < 255:
			for cam in Camera.CAMERAS:
				try:
					if Camera.keyManagement(chr(k), cam):
						return True
				except Exception as e: print e
		return False
	###
	
	# Liste des caméras
	CAMERAS = set()
	
	# Constructeur
	def __init__(this, **kargs):
		"""Constructor"""
		
		# On stocke la caméra dans un ensemble
		Camera.CAMERAS.add(this)
		
		# Objet fourre-tout
		this.PYON = pyon()
		
		# Objet de capture de la cam
		this._CAP = None
		
		# Fonction ++
		this.onFrameGet = lambda x: x
		
		# Coordonnées de la caméra
		this._POS = D2Point()
		
		# Coordonnées du repère
		this._SPACE = pyon(unknown=2)
		
		# Angles (w:x/h:y) de la caméra
		# EN RADIANS !!
		this._FOV = D2Point()
		
		# Image band + vertical resolution
		this._BAND = D2Point(0, 1)
		this._RES = 1 # (saut entre les lignes)
		
		# Dernière image capturée
		this._FRAME = Empty()
		
		# Image binaire rendue par les détections
		this._BINARY = Empty(channels=1)
		
		# Dernière image de scan calculée
		this._SCAN = Empty()
		
		# Dernière detection
		this._DETECTED = None
		
		# Clic
		this._BOTTOM = False
		
		# Image de référence (pas forcément utilisé, selon l'algo)
		this._REF = Empty()
		
		# Matrice de flou
		this._KERNEL = None
		
		# Objet de suppression d'arrière plan
		this._MOG2 = cv2.createBackgroundSubtractorMOG2(detectShadows=False, **kargs)
		
		# Image de soustraction d'arrière plan
		this._FGMASK = Empty(channels=1)
		
		# Kernel pour le débruitage
		this._ANOISEK = None
		
	# Destruction de la caméra (del this)
	def __del__(this):
		"""Destructor (del this)"""
		Camera.CAMERAS.remove(this)
		this.release()
	
	# Pour récupérer un paramètre facilement
	def getProp(this, prop):
		"""Getting camera's property"""
		this.checkInit()
		return this._CAP.get(Camera.props.get(prop, prop))
	
	# On règle le truc tranquille
	def setProp(this, prop, value):
		"""Setting camera's property"""
		this.checkInit()
		this._CAP.set(Camera.props.get(prop, prop), value)
	
	def Export(this, name):
		with open(name+'.config', 'w') as f:
			data = str(pyon(
				space = this._SPACE,
				pos = ~this._POS
			)); f.write(data)
			print '%s OK' % (data,)
			
	def Import(this, name):
		config = pyon()
		with open(name+'.config', 'r') as f:
			config.load(f.read())
		this._SPACE.load(config.space)
		this._POS = D2Point(*config.pos)
		print str(config) + ' Done.'
	
	# ------------------------------------------------------- # ------------------------------------------------------- #
	# Là on commence la race de getters...
	
	@property
	def exposure(this): return this.getProp('exposure')
	
	@property
	def height(this): return this.getProp('height')
	
	@property
	def width(this): return this.getProp('width')
	
	@property
	def fps(this): return this.getProp('fps')
	
	@property
	def fov(this): return this._FOV
	
	@property
	def position(this): return this._POS
	
	@property
	def space(this): return this._SPACE
	
	@property
	def capture(this): return this._CAP
	
	@property
	def frame(this):
		"""Last captured image"""
		return this._FRAME
	
	@property
	def reference(this):
		"""Reference image"""
		return this._REF
	
	@property
	def finger(this):
		"""Detected finger position"""
		return this._DETECTED
		
	@property
	def clic(this):
		"""Detected virtual click"""
		return this._BOTTOM
	
	@property
	def binary(this):
		"""Thresholded image (black/white, 3 channels)"""
		return this._BINARY
		
	@property
	def scan(this):
		"""Scanned image (often from 'binary')"""
		return this._SCAN
	
	# Reset de l'isolement
	def resetBin(this):
		"""Reset the binary image"""
		this._BINARY = EmptyFrom(this._FRAME, 1)
		
	# Affichage "complexe"
	@property
	def stream(this):
		"""Displays the scan and the current frame"""
		scan = this._SCAN
		frame = this._FRAME
		return np.bitwise_or(np.bitwise_and((np.logical_not(scan) * 255).astype(np.uint8), frame), scan)
		
	# ------------------------------------------------------- # ------------------------------------------------------- #
	
	# Pour configurer et démarrer la cam
	def init(this, id, **kargs):
		"""Capture and camera initialisation"""
		if this._CAP: this.release()
		this._CAP = cv2.VideoCapture(id)
		this.config(**kargs)
		
		this._CAP.set(cv2.CAP_PROP_FPS, 9999.9) # > 9000.
		
		try: this.getFrame()
		except:
			print 'On a perdu une caméra !'
			this.release()
	
	# Pour configurer la camera
	def config(this, **kargs):
		"""Camera's configuration:
		 - exposure: value < 0, brigther towards 0
		 - height: camera's capture height
		 - width: camera's capture width
		 - fps: camera's frenquency
		"""
		this.checkInit()
		result = {}
		
		# Récupérer la config totale
		if kargs.get('get', False):
			for prop in Camera.props: result[prop] = this.getProp(prop)
			return result
		
		# Si l'argument passé est une liste de paramètres
		kargs = kargs.get('params', kargs) # Ouch
		
		# On assigne les valeurs et on récupère le retour
		for param, value in kargs.iteritems(): this.setProp(param, value)
		for param in kargs: result[param] = this.getProp(param)
		
		# Résultat
		return result
	
	# On teste si la camera est initialisée
	def isInit(this):
		"""Is the device capturing ?"""
		return not not this._CAP
		# Who's here ?
		# - Me, I kill you.
	
	# On crash si la cam n'est pas lancée
	def checkInit(this):
		"""Crash if not capturing"""
		if not this._CAP: raise Exception('Vous devez initialiser la caméra...')
	
	# Pour lister les modes d'une caméra
	def getModes(this):
		"""Tries to list availables modes for the webcam"""
		this.checkInit()
		
		# On sauvegarde la config actuelle
		init = this.config(get=True)
		
		# Ensembles de modes
		formats = Camera.formats.copy()
		modes = set()
		
		# On averti du départ
		print '\nLooping modes for the camera... (%d modes)' % (len(formats))
			
		# Pour chaques formats
		while formats:
			
			# On récupère le format à tester
			format = formats.pop()
			
			# Configuration actuelle
			mode = this.config(
				height = float(format[1]),
				width = float(format[0])
			)
			
			# On enregistre le mode
			currentFormat = (mode['width'], mode['height'])
			modes.add(currentFormat)
			if currentFormat in formats:
				formats.remove(currentFormat)
			
			# On affiche l'itération courante
			printf('%d%5s\r' % (len(formats), ''))
		###
		
		# On remet comme avant et on retourne la liste de modes
		this.config(params=init); print 'Done, found %d.' % (len(modes))
		return [(int(mode[0]), int(mode[1])) for mode in modes]
	
	# On règle le morceau d'image à découper
	def setImageVertBand(this, a=0, b=1, r=1):
		"""When capturing a frame, cutting a chunk of the image:
		(from top to bottom)
		 - a: top limit [0;1]
		 - b: bottom limit [0;1]
		 - r: pixel jump (int)
		"""
		this._BAND = D2Point(a, b)
		this._RES = int(r)
	
	# On règle les dimensions angulaires
	# EN RADIANS !!
	def setFOV(this, **kargs):
		"""Camera's field of view (radians!):
		 - horizontal: obvious
		 - vertical: seriously ?
		"""
		this._FOV.x = kargs.get('horizontal', 0.0)
		this._FOV.y = kargs.get('vertical', 0.0)
	
	# On règle le niveau de lissage (floutage)
	def setBlurSize(this, size):
		"""Set blur kernel, number of pixels around to average"""
		this._KERNEL = np.ones((size, size), np.float32) / (size**2)
	
	# On récupère une frame (ou une portion selon la config)
	def getFrame(this, error=3, **kargs):
		"""Frame retreiving and formatting
		 - noReset: do not reset binary image (True/False)
		 - error: times to tryhard
		"""
		this.checkInit()
		
		# Arguments
		error = kargs.get('error', 3)
		noReset = kargs.get('noReset', False)
		
		# """
		while error >= 0:
			ret, frame = this._CAP.read()
			if ret:
				a = this._BAND.x * height(frame)
				b = this._BAND.y * height(frame)
				frame = frame[a:b:this._RES,:,:]
				if this._KERNEL is not None: # On applique un flou uniquement pour lisser le bruit
					frame = cv2.filter2D(frame, -1, this._KERNEL)
				this._FRAME = this.onFrameGet(frame)
				break #bye
			
			# On a pas eu d'image...
			else: error -= 1
			
		# On doit reset ou pas ?
		if not noReset: this.resetBin()
		return ret
	
	# def setReferenceSP(this, **kargs):
	
		# tolerance = kargs.get('tolerance', 20)
		# gamma = kargs.get('gamma', 1)

		# this.getFrame()
		# curr_frame = cf.Gamma(this._FRAME, gamma)
		# this._REF = curr_frame
		# this.maxes = curr_frame
		# this.mines = curr_frame

		# for i in range(9):
			# this.getFrame()
			# curr_frame = cf.Gamma(this._FRAME, gamma)
			# this._REF = this._REF / 2 + curr_frame / 2
			# this.maxes = np.maximum(this.maxes, curr_frame)
			# this.mines = np.minimum(this.mines, curr_frame)
			
		# this.tolerance_maxes = (this.maxes.astype(np.int32) + tolerance).clip(0, 255).astype(np.uint8)
		# this.tolerance_mines = (this.mines.astype(np.int32) - tolerance).clip(0, 255).astype(np.uint8)
		
	def setReferenceSP(this, **kargs):
		count = kargs.get('count', 10)
		
		this.setReference(count=count)
		ref_deriv = cf.Scharr(this.reference)
		ref_deriv = cf.Gamma(ref_deriv, this.PYON.gamma)
		ref_deriv_mask = ((ref_deriv > this.PYON.deriv_thresh) * 255).astype(np.uint8)
		this.ref_deriv = ref_deriv & ref_deriv_mask
		this.ref_deriv = cv2.erode(this.ref_deriv, (9, 9))
		this.ref_deriv = cv2.dilate(this.ref_deriv, (9, 9))
		
	# def st(this, cam, **kargs):
	
		# gamma = kargs.get('gamma', 1)
		# thresh = kargs.get('tolerance', this.PYON.tolerance)
		# med = kargs.get('med', 3)
	
		# cam.getFrame()
		
		# curr_frame = cf.Gamma(cam._FRAME, gamma)
		# valid_pixels_mask = np.logical_and(curr_frame > cam.mines, curr_frame < cam.maxes) * 255
		# over_pixels_mask = np.logical_and(curr_frame >= cam.maxes, curr_frame <= cam.tolerance_maxes) * 255
		# under_pixels_mask = np.logical_and(curr_frame >= cam.tolerance_mines, curr_frame <= cam.mines) * 255
		# unknown_over_mask = (curr_frame > cam.tolerance_maxes) * 255
		# unknown_under_mask = (curr_frame < cam.tolerance_mines) * 255
		# corrected_frame = (curr_frame & valid_pixels_mask) + (cam.maxes & over_pixels_mask) + (cam.mines & under_pixels_mask) + (curr_frame & unknown_over_mask) + (curr_frame & unknown_under_mask)
		
		# diff = cv2.absdiff(corrected_frame.astype(np.uint8), cam._REF)
		# result = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		# cam._BINARY = ((result >= thresh) * 255).astype(np.uint8)
		# cam._BINARY = cv2.medianBlur(cam._BINARY, med)
		# cam.arounder(
			# maxCount=1000,
			# minArea=64,
			# maxDist=1,
			# thick=1
		# )
		
	def st(this, cam, **kargs):	
		cam.getFrame()
		corrected_frame = cam.reference.copy()
		deriv = cf.Scharr(cam.frame)
		deriv = cf.Gamma(deriv, cam.PYON.gamma)
		deriv_mask = ((deriv > cam.PYON.deriv_thresh) * 255).astype(np.uint8)
		deriv = deriv & deriv_mask
		deriv = cv2.erode(deriv, (9, 9))
		deriv = cv2.dilate(deriv, (9, 9))
		
		for y in xrange(0, deriv.shape[0], cam.PYON.blockSize.height):
			for x in xrange(0, deriv.shape[1], cam.PYON.blockSize.width):
				ref_deriv_part = cam.ref_deriv[y:y+cam.PYON.blockSize.height, x:x+cam.PYON.blockSize.width]
				deriv_part = deriv[y:y+cam.PYON.blockSize.height, x:x+cam.PYON.blockSize.width]
				
				deriv_diff = abs(int(ref_deriv_part.sum()) - int(deriv_part.sum())) / float(cam.PYON.blockSize.width * cam.PYON.blockSize.height * 3 * 255)
				
				if deriv_diff >= cam.PYON.deriv_diff_thresh:
					corrected_frame[y-cam.PYON.spread:y+cam.PYON.blockSize.height+cam.PYON.spread, x-cam.PYON.spread:x+cam.PYON.blockSize.width+cam.PYON.spread] = cam.frame[y-cam.PYON.spread:y+cam.PYON.blockSize.height+cam.PYON.spread, x-cam.PYON.spread:x+cam.PYON.blockSize.width+cam.PYON.spread]
				#end if
			# end if
		# end for
		
		diff = cv2.absdiff(corrected_frame, cam.reference)
		diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		diff = ((diff > cam.PYON.thresh) * 255).astype(np.uint8)
		
		cam._BINARY = diff.copy();
	
		cam.arounder(
			maxCount=1000,
			minArea=64,
			maxDist=5,
			thick=1
		)
	
	# On stocke l'image de référence
	def setReference(this, **kargs):
		"""Save frame as reference
		 - interval: time between takes (ms)
		 - count: number of frame to take
		"""
		
		# Arguments
		sumSeuil = kargs.get('sumSeuil', 200)
		refSeuil = kargs.get('refSeuil', 150)
		interval = kargs.get('interval', 0)
		check = kargs.get('check', False)
		count = kargs.get('count', 1)
		
		# Image cumulative
		cumul = None
		
		# Capture image par image
		if count > 1: printf('Prise de reference sur %d prises... ' % count)
		for i in xrange(count):
			if i and interval: time.sleep(interval/1000)
			
			# Prise d'image
			this.getFrame()
			
			# Référence actuelle
			current = this._FRAME
			
			if i: # Si ce n'est plus la première itération
				
				if check:
					# Détection d'un changement
					this.detectByRef(seuil=refSeuil, ref=result, frame=current)
					sum = this.binary.sum()/255
					if sum > sumSeuil: # Crash
						raise Exception("Don't interfere with the reference ! (%d)" % sum)
				# END CHECK
				
				# Cumulation
				cumul += current
			
			else: # Première itération
				cumul = current.astype(int)
				
			# Calcul de l'image moyenne actuelle
			result = (cumul / (i+1)).astype(np.uint8)
		###
		
		this.resetBin()
		this._REF = result
		if count > 1: print 'ok'
		return result
	
	# Exposure calibration
	def autoExposure(this, **kargs):
		"""Tryies to maximize entropy"""
		
		# Arguments
		frames = kargs.get('frames', 4)
		start = kargs.get('start', -10)
		end = kargs.get('start', -3)
		
		max = 0
		v = start
		print 'Auto Exposition starting...'
		
		for i in range(start, end):
			this.setProp('exposure', i)
			for j in range(frames): this.getFrame()
			
			e = imEntropy(this.frame)
			if e > max:
				max = e
				v = i
		
		this.setProp('exposure', v)
		for j in range(frames): this.getFrame()
		print 'Exposure Calibrated: %i / Entropy: %.4f' % (v, max)
	
	# On affiche la tarte aux pommes
	def drawSpace(this, **kargs):
		"""Call me maybe"""
		
		space = this._SPACE
		if not space: return None
		
		scan = this._SCAN
		w = width(scan)
		
		# Impression
		scan[:, (1 - space.o) * w, :] = [255, 255, 0]
		scan[:, (1 - space.i) * w, :] = [0, 255, 255]
		scan[:, (1 - space.j) * w, :] = [255, 0, 255]
		return True
	
	# On récupère la position détectée puis RàZ
	def grabDetected(this):
		"""Read and erase last finger position"""
		grab, this._DETECTED = this._DETECTED, None
		return grab
	
	# On arrête la capture du flux
	def release(this):
		"""Stop capturing"""
		this._CAP.release()
		
	# On stop toutes les caméras
	@staticmethod
	def releaseAll():
		"""Stop evrything"""
		for cam in Camera.CAMERAS: cam.release()
	
	# On coupe tout
	@staticmethod
	def closeCamApp():
		"""Stop capturing and destroy cv2 windows"""
		Camera.releaseAll()
		cv2.destroyAllWindows()
	
	# ------------------------------------------------------- # ------------------------------------------------------- #
	
	# On filme tout
	@staticmethod
	def getFrames():
		"""Get frames from all camera"""
		for cam in Camera.CAMERAS: cam.getFrame()
	
	# Si une droite d' est parallèle à une droite d, et une droite d" à la droite d', alors d et d" sont parallèles.
	@staticmethod
	def AsyncProcess(**kargs):
		"""Start image process:
		"""
		
		# Arguments
		cams = kargs.get('cams', Camera.CAMERAS)
		func = kargs.get('func', lambda cam: None)
		
		threads = []
		for cam in cams:
			thread = Thread(target=func, args=(cam,))
			threads.append(thread)
			thread.start()
			
		# On synchronise
		for thread in threads: thread.join()
	
	# ------------------------------------------------------- # ------------------------------------------------------- #
	
	# Pour calibrer la caméra
	def calibrate_old(this, display=False): # C'est des maths.
		"""Sets camera's position according to the space"""
		# a -> Angle Alpha
		# b -> Angle Beta
		
		# Verif de l'espace
		space = this._SPACE
		if not space: return None
		
		#try:
		try:
		
			# Calcul d'angles
			a = this._FOV.x * (space.i - space.o)
			b = this._FOV.x * (space.o - space.j)
		
			# On essaye gentillement
			Ca = 1 - 1.0/math.tan(a)
			Cb = 1 - 1.0/math.tan(b)
			k = Cb/Ca
			
			# Position finale
			this._POS.x = x = (1 + k / math.tan(a)) / (1 + k**2)
			this._POS.y = x * k
		
		# Erm
		except: this._POS = None
		
		# Petit affichage oklm
		if display: print 'Calibration: %f %f %s' % (math.degrees(a), math.degrees(b), ~this._POS)
		return this._POS
	
	# Pour calibrer la caméra
	def calibrate(this, display=False, **kargs): # C'est des maths.
		"""Sets camera's position according to the space"""
		# a -> Angle Alpha
		# b -> Angle Beta
		
		h = float(kargs.get('h', 1))
		w = float(kargs.get('w', 1))
		
		# Verif de l'espace
		space = this._SPACE
		if not space: return None
		
		#try:
		try:
		
			# Calcul d'angles
			a = this._FOV.x * (space.i - space.o)
			b = this._FOV.x * (space.o - space.j)
		
			# On essaye gentillement
			Ca = w - h / math.tan(b)
			Cb = h - w / math.tan(a)
			kx = Ca/Cb
			
			# Position finale
			this._POS.x = x = h * (kx + 1 / math.tan(b)) / (1 + kx**2)
			this._POS.y = x * kx
		
		# Erm
		except: this._POS = None
		
		# Petit affichage oklm
		if display: print 'Calibration: %f %f %s' % (math.degrees(a), math.degrees(b), ~this._POS)
		return this._POS
	
	# Pour obtenir l'angle absolu du doigt par rapport à l'origine
	@property # Oui c'est moche, mais ça marche.
	def fingerAbsoluteAngle(this):
		"""Finger's absolute angle relative to the space"""
		if not this.finger: return None
		
		_180 = math.radians(180.0)
		finger = this.finger.x * this._FOV.x
		O = this._SPACE.o * this._FOV.x
		
		# Angle calculé à partir des coordonnées de la caméra
		if this._POS.x: offset = math.atan(this._POS.y / this._POS.x)
		elif this._POS.y > 0: offset = math.radians(90.0)
		elif this._POS.y < 0: offset = math.radians(-90.0)
		else: offset = 0
			
		return (_180 + offset) - (O - finger)
	
	# Pour déduire la position d'un doigt entre deux caméras
	def fingerPosition(this, cam):
		"""Return's finger position depending on the two camera's data
			Return values:
			 - click (bool)
			 - position (D2Point)
		"""
		
		# 'cam' doit être de type 'Camera'
		if not isinstance(cam, Camera): raise Exception("Operation uniquement possible sur un objet de type 'Camera'...")
		
		# Tout doit être calibré et detecté, sinon on peut pas
		if not (this.finger and cam.finger and this.position and cam.position): return (False, None)
		
		try: # Ca peut foirer
			a = math.tan(this.fingerAbsoluteAngle)
			b = this.position.y - a * this.position.x
			
			c = math.tan(cam.fingerAbsoluteAngle)
			d = cam.position.y - c * cam.position.x
			
			x = (d - b) / (a - c)
			y = a * x + b
		
		# Catch !
		except: return (False, None)
		
		# Si les doigts sont détectés à la position minimale
		click = (this.clic and cam.clic)
		
		# Si ya click
		return (click, D2Point(x, y))
		
	# Simplification (cam1 % cam2)
	def __mod__(this, cam): return this.fingerPosition(cam)
	
	# ------------------------------------------------------- # ------------------------------------------------------- #
	
	# Traitement de l'image
	# Algo par détection de couleur
	def detectByColor(this, **kargs):
		"""Color thresholding:
		 - hueLowMin: 
		 - hueLowMax: 
		 - hueHighMin: 
		 - seuil: 
		 - blur: Blur the result image
		"""
		
		# Arguments
		hueLowMin = kargs.get('hueLowMin', 1)
		hueLowMax = kargs.get('hueLowMax', 21)
		hueHighMin = kargs.get('hueHighMin', 170)
		seuil = kargs.get('seuil', 100)
		blur = kargs.get('blur', False)
		
		# Image source
		src = this._FRAME
		
		# Résultat
		bin = this._BINARY
		
		# Les espaces de couleurs tré poussver
		hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
		lab = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)
		ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
		luv = cv2.cvtColor(src, cv2.COLOR_BGR2Luv)
		
		# Détecteur thermique
		hue = hsv
		hue[:,:,1] = 255
		hue[:,:,2] = 255
		hue = cv2.cvtColor(hue, cv2.COLOR_HSV2BGR)
		
		# Seuillage sur le h
		h = hsv[:,:,0] #hsv
		h = np.logical_or(np.logical_and(h > hueLowMin, h < hueLowMax), h > hueHighMin) * 255 #hsv
		
		# Seuillages complètement random sur les autres canaux
		a = (lab[:,:,1] > 130) * 255 #lab
		cr = (ycrcb[:,:,1] > 145) * 255 #ycrcb
		
		# Résultat moyen
		result = (h/3 + a/3 + cr/3)
		if blur: # Pour lisser le bruit
			kernel = np.ones((3, 3), np.float32)/9
			result = cv2.filter2D(result.astype(np.uint8), -1, kernel)
		
		# Résultat
		this._BINARY = bin = np.zeros((height(this._FRAME), width(this._FRAME)), np.uint8)
		bin[:,:] = (result > seuil) * 255
		
		return pyon(
			thermal = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR),
			total = result.astype(np.uint8),
			result = bin.astype(np.uint8),
			cr = cr.astype(np.uint8),
			h = h.astype(np.uint8),
			a = a.astype(np.uint8)
		)
	
	# Traitement de l'image
	# Algo par différence d'image
	def detectByRef(this, **kargs):
		"""Reference/difference thresholding:
		 - seuil: threshold on the sum of the absolute difference of pixels between images
		"""
		
		# Arguments
		seuil = kargs.get('seuil', 100)
		frame = kargs.get('frame', this._FRAME)
		ref = kargs.get('ref', this._REF)
		
		# On fait la différence et on extrait les composantes RGB
		# diff = cv2.absdiff(frame, ref)
		diff = np.abs(frame.astype(int) - ref.astype(int)).astype(np.uint8)
		
		# Petit seuillage des familles
		this._BINARY = delta = EmptyFrom(diff, 1)
		delta[:,:] = (diff.sum(axis=2) > seuil) * 255
		
		return pyon(
			AbsDiff = diff,
			Threshold = delta
		)
		
	# Différence avec pesage de la luminosité
	def detectByRefAdv(this, **kargs):
		"""Tryies to weight difference by looking at the reference intensities (per pixel)
		"""
		
		# Arguments
		seuil = kargs.get('seuil', 100)
		ref = kargs.get('ref', this._REF)
		frame = kargs.get('frame', this._FRAME)
		coef = kargs.get('coef', 1)
		
		# On fait la différence et on extrait les composantes RGB
		diff = cv2.absdiff(frame, ref)
		
		# Zblah
		sat = diff.copy()
		weight = 1 + (cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY) / 255.0) * coef
		sat[:,:,0] *= weight
		sat[:,:,1] *= weight
		sat[:,:,2] *= weight
		
		# Petit seuillage des familles
		this._BINARY = delta = EmptyFrom(sat, 1)
		delta[:,:] = ((sat[:,:,2] + sat[:,:,1] + sat[:,:,0]) > seuil) * 255
		
		return pyon(
			AbsDiff = diff,
			Weight = weight % 1,
			Weighted = sat,
			Threshold = delta
		)
		
	# Traitement de l'image
	# Algo chelou proposé par Estelol
	def detectHybrid(this, **kargs):
		"""Hybrid thresholding:
		 - hueLowMin: 
		 - hueLowMax: 
		 - hueHighMin: 
		 - seuilColor: 
		 - seuilDiff: 
		"""
		
		# Arguments
		hueLowMin = kargs.get('hueLowMin', 1)
		hueLowMax = kargs.get('hueLowMax', 10)
		hueHighMin = kargs.get('hueHighMin', 170)
		seuilColor = kargs.get('seuilColor', 200)
		seuilDiff = kargs.get('seuilDiff', 50)
		
		# Image source
		src = this._FRAME
		
		# Les espaces de couleurs tré poussver
		hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
		lab = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)
		ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
		luv = cv2.cvtColor(src, cv2.COLOR_BGR2Luv)
		
		# Détecteur thermique
		hue = hsv
		hue[:,:,1] = 255
		hue[:,:,2] = 255
		hue = cv2.cvtColor(hue, cv2.COLOR_HSV2BGR)
		
		# Seuillage sur le h
		h = hsv[:,:,0] #hsv
		h = np.logical_or(np.logical_and(h > hueLowMin, h < hueLowMax), h > hueHighMin) * 255 #hsv
		
		# Seuillages complètement random sur les autres canaux
		a = (lab[:,:,1] > 130) * 255 #lab
		cr = (ycrcb[:,:,1] > 145) * 255 #ycrcb
		
		# On fait la différence et on extrait les composantes RGB
		diff = np.abs(this._FRAME.astype(int) - this._REF.astype(int))
		
		# Petit seuillage des familles
		this._BINARY = bin = np.zeros((height(diff), width(diff)), np.uint8)
		delta = ((diff[:,:,2] + diff[:,:,1] + diff[:,:,0]) > seuilDiff) * 255
		
		result = (h/3 + a/3 + delta/3)
		bin[:,:] = (result > seuilColor) * 255
		
		return pyon(
			result = this._SCAN.astype(np.uint8),
			total = result.astype(np.uint8),
			delta = delta.astype(np.uint8),
			diff = diff.astype(np.uint8),
			cr = cr.astype(np.uint8),
			h = h.astype(np.uint8),
			a = a.astype(np.uint8)
		)
	
	# Magnifique idée de Maxou, pas compliqué en plus !
	# Saber: On additionne toutes les colonnes de 'binary'
	# Et on threshold !
	def saber(this, **kargs):
		"""Vertical object detection:
		Slice vertically and mesures height
		 - threshold: (the minimum height of an object
			x =< 1: Relative to image height
			x > 1: Pixels
		"""
		
		# Arguments
		bin = kargs.get('bin', this._BINARY)
		thresh = kargs.get('thresh', 0.5) # Seuillage hauteur
		thresh = tresh if thresh > 1 else thresh * height(bin)
		
		# Somme verticale et seuillage
		vsum = (bin!=0).sum(axis=0) >= thresh
		
		# Envoi du résultat dans la pipeline
		bin[:,:] = vsum * 255
		#this._BINARY = vsum
	
	# Utilisation du MOG2: Extraction
	def fgExtract(this, **kargs):
		"""Isolate the foreground
		"""
		this._FGMASK = fgmask = this._MOG2.apply(this._FRAME)
		return fgmask
	
	# Utilisation du MOG2: Addition
	def fgCompensate(this, **kargs):
		"""Apply logical 'or' to the original detection and foreground mask
		"""
		this._BINARY = bin = (np.logical_or(this._BINARY, this._FGMASK) * 255).astype(np.uint8)
		return bin
	
	# Mode auto
	def fgMagic(this, **kargs):
		"""Simplifaction, do the followings:
		 * fgExtract
		 * fgCompensate
		"""
		this.fgExtract()
		this.fgCompensate()
		return 'Magic !'
		
	# Création du kernel de traitement
	def setAnoisek(this, **kargs):
		"""Creates the kernel for de-noising
		 - radius: kernel's radius
		"""
		
		# Arguments
		radius = kargs.get('radius', 3)
		
		# Kernel magic
		this._ANOISEK = kernel = anoisek(radius)
		return kernel
		
	# Truc de ouf
	def anoise(this, *args, **kargs):
		"""Tries to denoise the binary output
		 ! You need to call 'this.setAnoisek' !
		"""
		
		# Arguments
		if not args: args = [50]
		
		# Kernel's retrieval
		anoisek = this._ANOISEK
		if anoisek is None: return None
		
		# More magic
		bin = this._BINARY
		for thresh in args:
			bin[:,:] = (cv2.filter2D(bin, -1, anoisek) / 2.55 > thresh) * 255
		return True
	
	# ------------------------------------------------------- # ------------------------------------------------------- #
	
	# Pour localiser le doigt sur une image binaire (noir/blanc)
	# Skywalker: On compte le nombre de pixels sur une ligne en
	# autorisant d'avancer dans le vide sur une distance donnée
	def skywalker(this, **kargs):
		"""Object detection in binary image by straight cut
		Allow cutting for a bit through void:
		 - offshore: distance allowed in the void to look
		 - minSize: (the minimum size of an object)
			x < 1: Relative to image width
			x > 1: Pixels
		 - bin: binary image to parse (3 channel matrix)
		 - blur: add blur on 'bin' ? (bool)
		"""
		
		# Arguments
		bin = kargs.get('bin', this._BINARY)
		offshore = kargs.get('offshore', 5)
		minSize = kargs.get('minSize', 3)
		blur = kargs.get('blur', False)
		
		if blur: # Flou de test
			kernel = np.ones((3, 3), np.float32)/9
			bin = cv2.filter2D(bin, -1, kernel)
		
		# On duplique l'image pour le rendu final
		scan = EmptyFrom(bin, 3)
		scan[:,:,0] = scan[:,:,1] = scan[:,:,2] = bin
		this._SCAN = scan
		
		step = 0 # Compteur de pas dans le vide
		start, end = None, None
		
		# Dimensions de l'image à scanner
		size = D2Point(width(bin), height(bin))
		ratio = size if minSize < 1 else 1
		
		# Scan pixel par pixel, en partant du bas
		for v in xrange(int(size.y)-1, -1, -1):
			for u in xrange(int(size.x)):
			
				if bin.item((v, u)): # Si un pixel != 0:
					scan[v,u] = [0, 0, 255] # Rouge.
					step = 0 # On reset le jump
					
					# Si c'est le premier
					if not start:
						start = D2Point(u, v)
						end = D2Point(u, v)
					else: # On trace
						end.x, end.y = u, v
				
				elif end:
					if step < offshore:
						scan[v,u] = [0, 255, 255] # Jaune
						step += 1 # On continue
					elif abs((start - end)/ratio) < minSize:
						start, end = None, None
					else: break
				# elif end: break
			###
			if end: break
		###
		
		if end: # Si on a trouvé une fin
			
			# Point médian = doigt
			result = start % end
			
			# Visuel
			scan[:,result.x,:] = [0, 255, 0] # On trace une bande verte
			scan[result.y,:,:] = [0, 127, 0] # On trace une autre bande verte
			
			# Reformatage
			result /= size-1 # On remet en ratio d'image
			result.x = 1 - result.x # On inverse le côté de mesure
			
			# Stockage
			this._DETECTED = result # On stocke le point détecté
			this._BOTTOM = result.y == 1 # On clic ou bien ?
		
		# Si rien
		else:
			result = None
			this._BOTTOM = False
		
		# Tchao
		return result
	
	# Algorithme de détection de countours
	def arounder(this, **kargs):
		"""Function making use of OpenCV's contours.
		 - maxCount: Maximum number of contours to process
		 - minArea: Minimum area to look for
		 - maxArea: Maximum area to look for
		 - ignore: Painting color for ignored contours
		 - color: Painting color for accepted contours
		 - thick: Lines thickness
		"""
		
		# Arguments
		maxCount = kargs.get('maxCount', 200)
		maxArea = kargs.get('maxArea', 10000000)
		minArea = kargs.get('minArea', 0)
		maxDist = kargs.get('maxDist', 0)
		ignore = kargs.get('ignore', (0, 255, 0))
		color = kargs.get('color', (0, 0, 255))
		thick = kargs.get('thick', 1)
		
		# Image binaire issue de la détection
		bin = this._BINARY.copy()
		input = bin.copy()
		
		# Modifie l'image de départ T__T
		image, contours, hierarchy = cv2.findContours(
			input,
			cv2.RETR_LIST,
			cv2.CHAIN_APPROX_SIMPLE
		)
		
		# Comptation
		finger = None
		count = len(contours)
		objects, ignored = [], []
		if count < maxCount: #raise Exception('Too much noise, please quiet.')
			
			# Filtrage et localisation:
			for contour in contours:
				
				# Filtrage des contours selon l'aire
				area = cv2.contourArea(contour)
				if minArea <= area and area <= maxArea:
					
					# Calcul de la position
					obj = cv2.convexHull(contour)
					point = limiter(obj, maxDist)
					
					# Est-ce le point le plus bas ?
					if finger:
						if finger.y < point.y: finger = point
					else: finger = point
					
					# Enregistrement
					objects.append(obj)
				
				# Sinon on l'ignore
				else: ignored.append(contour)
				
			### END FOR
		
		### END IF
		else: ignored = contours
		
		# On duplique l'image pour le rendu final
		this._SCAN = scan = EmptyFrom(bin, 3)
		scan[:,:,0] = scan[:,:,1] = scan[:,:,2] = bin
		
		# Visuel
		printf('%d/%d%60s\r' % (len(objects), count, ''))
		cv2.drawContours(scan, ignored, -1, ignore, 1)
		cv2.drawContours(scan, objects, -1, color, thick)
		
		# Si on a trouvé
		if finger:
			
			# Affichage viseur
			scan[:, finger.x, :] = [255, 0, 0]
			scan[finger.y, :, :] = [127, 0, 0]
			
			# Calcul de la taille de l'image
			size = D2Point(width(bin), height(bin))
			
			# Reformatage
			origin = +finger
			finger /= size-1
			finger.x = 1 - finger.x
			this._BOTTOM = (origin-2).y == (size-4).y
		
		# Sinon on arrête de cliquer
		else: this._BOTTOM = False
		
		# On enregistre le truc
		this._DETECTED = finger
		
		return pyon(
			contours = scan
		)
###"""

# Si un débile lance le module directement
if __name__ == '__main__':
	try: from getch import getch
	except: pass
	try: from msvcrt import getch
	except: pass
	print "C'est une sorte de librairie, faut pas l'executer comme ca :O"
	print "Mais tout se passe bien visiblement..."
	try: getch()
	except: raw_input()