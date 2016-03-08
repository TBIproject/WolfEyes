# -*- coding: utf-8 -*-
import sys
OUT = sys.stdout
NUL = open('nul', 'w')

# Sauvegarde de l'état initial
START = set(dir())

# On capture tout dans le vide
sys.stdout = NUL

# Importations
from .. import MouseControl
from .. import CustomFilter
from ..camera import Space, Camera
from ..D2Point import D2Point
from ..tbiTools import *
from ..pyon import pyon
import numpy
import math
import time
import cv2

# Raccourcis
np = numpy
cf = CustomFilter
mouse = MouseControl

# On remet comme ça va bien
sys.stdout = OUT
NUL.close()

# Etat final (après imports)
END = set(dir())

# __all__ = ['Space', 'Camera', 'D2Point', 'pyon', 'MouseControl', 'mouse', 'math', 'time', 'cv2', 'numpy', 'np']
__all__ = list(START ^ END)
__all__.remove('START')