# this file is the game manager
# it's responsible for globals (helper functions, constants, etc)

import os, pygame
from pygame.locals import *
from structs       import Vector

DIR = os.path.abspath("")

PIXEL_SCALE = 2
TILE_SIZE   = 32

MAP_SIZE    = Vector(2*6 + 3, 2*5 + 3)
SCREEN_SIZE = MAP_SIZE * TILE_SIZE
WINDOW_SIZE = SCREEN_SIZE * PIXEL_SCALE

window = pygame.display.set_mode(WINDOW_SIZE.unpack())
screen = pygame.Surface(SCREEN_SIZE.unpack())
stage  = None

def new_image(path):
   return pygame.image.load(os.path.join(DIR, path)).convert_alpha()