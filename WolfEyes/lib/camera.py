# -*- coding: utf-8 -*-
# AUTHOR(S): POPOLO, 
# REQUIRE PYTHON 2.7x
# REQUIRE CV2 3.x
# NOTE: ON MESURE LES ANGLES DE DROITE A GAUCHE!
# NOTE: ON UTILISE LES ANGLES EN RADIANS!
import time # Owi
import math # OWI
import sys # YEAH
print sys.version # Utile
try: # On essaye d'importer cv2
	import cv2; v = cv2.__version__ # CV2 VERSION
	if v[0] != '3': print "OpenCV 3.x required, got %s..." % (v); exit()
	del v # tout propre
except: print 'OpenCV 3.x is required... Missing'; exit()

# On essaye d'importer NumPy
try: import numpy as np
except Exception as e: print e; exit()
# On essaye d'importer les outils
try: from tbiTools import *
except Exception as e: print e; exit()
# On essaye d'importer les points/vecteurs 2D
try: from D2Point import *
except Exception as e: print e; exit()

# Gestion du repère, en mesure d'angles relatifs
class Space():
	def __init__(this, o=0, i=0, j=0):
		this.o = float(o)
		this.i = float(i)
		this.j = float(j)

# """
# Easy cam
class Camera():
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
		return cv2.waitKey(t) & 0xFF
	
	# Liste des caméras
	CAMERAS = set()
	
	# Constructeur
	def __init__(this):
		"""Constructor"""
		
		# On stocke la caméra dans un ensemble
		Camera.CAMERAS.add(this)
		
		# Objet de capture de la cam
		this._CAP = None
		
		# Coordonnées de la caméra
		this._POS = D2Point()
		
		# Coordonnées du repère
		this._SPACE = Space()
		
		# Angles (w:x/h:y) de la caméra
		# EN RADIANS !!
		this._FOV = D2Point()
		
		# Image band + vertical resolution
		this._BAND = D2Point(0, 1)
		this._RES = 1 # (saut entre les lignes)
		
		# Dernière image capturée
		this._FRAME = Empty()
		
		# Image binaire rendue par les détections
		this._BINARY = Empty()
		
		# Dernière image de scan calculée
		this._SCAN = Empty()
		
		# Dernière detection
		this._DETECTED = None
		
		# Image de référence (pas forcément utilisé, selon l'algo)
		this._REF = Empty()
		
		# Matrice de flou
		this._KERNEL = None
	
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
	
	# ------------------------------------------------------- #
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
		this._BINARY = Empty()
		
	# ------------------------------------------------------- #
	
	# Pour configurer et démarrer la cam
	def init(this, id, **kargs):
		"""Capture and camera initialisation"""
		if this._CAP: this.release()
		this._CAP = cv2.VideoCapture(id)
		this.config(
			exposure=kargs.get('exposure', this.exposure),
			height=kargs.get('height', this.height),
			width=kargs.get('width', this.width),
			fps=kargs.get('fps', this.fps)
		)
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
	def getFrame(this, error=3):
		"""Frame retreiving and formatting"""
		this.checkInit()
		
		# """
		while error>=0:
			ret, frame = this._CAP.read()
			if ret:
				a = this._BAND.x * height(frame)
				b = this._BAND.y * height(frame)
				frame = frame[a:b:this._RES,:,:]
				if this._KERNEL is not None: # On applique un flou uniquement pour lisser le bruit
					this._FRAME = cv2.filter2D(frame, -1, this._KERNEL)
				else: this._FRAME = frame
				break #bye
			# On a pas eu d'image...
			else: error -= 1
		return ret
		"""
		ret, frame = this._CAP.read()
		if ret:
			a = this._BAND.x * height(frame)
			b = this._BAND.y * height(frame)
			frame = frame[a:b:this._RES,:,:]
			if this._KERNEL is not None: # On applique un flou uniquement pour lisser le bruit
				this._FRAME = cv2.filter2D(frame, -1, this._KERNEL)
			else: this._FRAME = frame
		return ret
		"""#"""
		
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
		count = kargs.get('count', 1)
		
		# Image cumulative
		cumul = None
		
		# Capture image par image
		if count > 1: print 'Prise de reference sur %d prises...' % count
		for i in xrange(count):
			if i and interval: time.sleep(interval/1000)
			
			# Prise d'image
			this.getFrame()
			
			# Référence actuelle
			current = this._FRAME
			
			if i: # Si ce n'est plus la première itération
			
				# Détection d'un changement
				this.detectByRef(seuil=refSeuil, ref=result, frame=current)
				sum = this.binary.sum()/255
				if sum > sumSeuil: # Crash
					raise Exception("Don't interfere with the reference ! (%d)" % sum)
				
				# Cumulation
				cumul += current
			
			else: # Première itération
				cumul = current.astype(int)
				
			# Calcul de l'image moyenne actuelle
			result = (cumul / (i+1)).astype(np.uint8)
		###
		
		this.resetBin()
		this._REF = result
		return result
	
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
	
	# ------------------------------------------------------- #
	
	# Pour calibrer la caméra
	def calibrate(this, display=False): # C'est des maths.
		"""Sets camera's position according to the space"""
		# a -> Angle Alpha
		# b -> Angle Beta
		a = this._FOV.x * (this._SPACE.i - this._SPACE.o)
		b = this._FOV.x * (this._SPACE.o - this._SPACE.j)
		
		try: # On essaye gentillement
			Ca = 1 - 1.0/math.tan(a)
			Cb = 1 - 1.0/math.tan(b)
			k = Cb/Ca
			
			this._POS.x = x = (1 + k / math.tan(a)) / (1 + k**2)
			this._POS.y = x * k
		
		# Erm
		except: this._POS = None
		
		# Petit affichage oklm
		if display: print 'Calibration: %f %f %s' % (math.degrees(a), math.degrees(b), this._POS)
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
		click = (this.finger.y == 0 and cam.finger.y == 0)
		
		# Si ya click
		return (click, D2Point(x, y))
		
	# Simplification (cam1 % cam2)
	def __mod__(this, cam): return this.fingerPosition(cam)
	
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
		this._SCAN = scan = bin.copy()
		
		step = 0 # Compteur de pas dans le vide
		start, end = None, None
		
		# Dimensions de l'image à scanner
		size = D2Point(width(bin), height(bin))
		ratio = size if minSize < 1 else 1
		
		# Scan pixel par pixel, en partant du bas
		for v in xrange(int(size.y)-1, -1, -1):
			for u in xrange(int(size.x)):
			
				if bin.item((v, u, 0)): # Si un pixel != 0:
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
					elif abs((start - end)/ratio) <= minSize:
						start, end = None, None
					else: break
				# elif end: break
			###
			if end: break
		###
		
		if end:
			result = start % end # Point médian = doigt
			scan[:,result.x,:] = [0, 255, 0] # On trace une bande verte
			scan[result.y,:,:] = [0, 127, 0] # On trace une autre bande verte
			result /= size # On remet en ratio d'image
			result.x = 1 - result.x # On inverse le côté de mesure
			this._DETECTED = result # On stocke le point détecté
		else: result = None
		return result
		
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
		this._BINARY = bin = np.zeros((height(this._FRAME), width(this._FRAME), 3), np.uint8)
		bin[:,:,0] = bin[:,:,1] = bin[:,:,2] = (result > seuil) * 255
		
		return {
			"thermal": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR),
			"total": result.astype(np.uint8),
			"result": bin.astype(np.uint8),
			"cr": cr.astype(np.uint8),
			"h": h.astype(np.uint8),
			"a": a.astype(np.uint8)
		}
	
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
		diff = np.abs(frame.astype(int) - ref.astype(int))
		
		# Petit seuillage des familles
		this._BINARY = delta = np.zeros((height(diff), width(diff), 3), np.uint8)
		delta[:,:,0] = delta[:,:,1] = delta[:,:,2] = ((diff[:,:,2] + diff[:,:,1] + diff[:,:,0]) > seuil) * 255
		
		return {
			'AbsDiff': diff.astype(np.uint8),
			'Threshold': delta.astype(np.uint8)
		}
		
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
		this._BINARY = bin = np.zeros((height(diff), width(diff), 3), np.uint8)
		delta = ((diff[:,:,2] + diff[:,:,1] + diff[:,:,0]) > seuilDiff) * 255
		
		result = (h/3 + a/3 + delta/3)
		bin[:,:,0] = bin[:,:,1] = bin[:,:,2] = (result > seuilColor) * 255
		
		return {
			"result": this._SCAN.astype(np.uint8),
			"total": result.astype(np.uint8),
			"delta": delta.astype(np.uint8),
			"diff": diff.astype(np.uint8),
			"cr": cr.astype(np.uint8),
			"h": h.astype(np.uint8),
			"a": a.astype(np.uint8)
		}
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