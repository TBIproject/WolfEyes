# -*- coding: utf-8 -*-
import sys, StringIO
OUT = sys.stdout
NUL = StringIO.StringIO()

# Sauvegarde de l'état initial
START = set(dir())

# On capture tout dans le vide
sys.stdout = NUL

# Importations
import tbiTools
import MouseControl
import CustomFilter
from camera import *
from D2Point import *
from pyon import *

# Raccourcis
cf = CustomFilter
mouse = MouseControl
tools = tbiTools

# On remet comme ça va bien
sys.stdout = OUT
NUL.close()

# Etat final (après imports)
END = set(dir())

# __all__ = ['camera', 'D2Point', 'tbiTools', 'pyon', 'MouseControl', 'CustomFilter']
__all__ = list(START ^ END)
__all__.remove('START')