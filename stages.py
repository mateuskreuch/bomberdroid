# this file contains the stages of the game
# stages are also commonly known as states or screens, and is basically a piece
# of the game

import gm, tobjs
from structs import Matrix

class Stage:
   def update(self, dt):        pass
   def draw(self):              pass
   def key_pressed(self, key):  pass
   def key_released(self, key): pass

class MainMenu(Stage):
   def __init__(self):
      self._bg = gm.new_image("gfx/tile_grass.png")

   def draw(self):
      gm.screen.blit(self._bg, (0, 0))

class Arena(Stage):
   def __init__(self):
      self._tiles = Matrix(gm.MAP_SIZE.x, gm.MAP_SIZE.y)
      self.tttt = 4

teste = Arena()