import os, pygame
from pygame.locals import *
from game_structs import Vector

DIR = os.path.abspath("")

PIXEL_SCALE = 2
TILE_SIZE   = 32

MAP_SIZE    = Vector(2*6 + 3, 2*5 + 3)
SCREEN_SIZE = MAP_SIZE * TILE_SIZE
WINDOW_SIZE = SCREEN_SIZE * PIXEL_SCALE

window = pygame.display.set_mode(WINDOW_SIZE.totuple())
screen = pygame.Surface(SCREEN_SIZE.totuple())
stage  = None

def new_image(path):
   return pygame.image.load(os.path.join(DIR, path)).convert_alpha()