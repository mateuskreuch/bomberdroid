import os, pygame
from pygame.locals import *

DIR = os.path.abspath("")

screen = None
stage  = None

def new_image(path):
   return pygame.image.load(os.path.join(DIR, path)).convert_alpha()