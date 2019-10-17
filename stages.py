# this file contains the stages of the game
# stages are also commonly known as states or screens, and is basically a piece
# of the game

import gm, tobjs
from structs import Matrix
from tiles import *

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
      self._player = gm.new_image("gfx/player.png")

      for x, y, _ in self._tiles:
         self._tiles.set(x, y, (
            self._tiles.is_inside(x - 1, y - 1) and
            self._tiles.is_inside(x + 1, y + 1) and
            (x % 2 == 1 or y % 2 == 1))
            and TlGrass()
            or  TlBrick())

   def draw(self):
      for x, y, value in self._tiles:
         if value is not None:
            gm.screen.blit(value.sprite, (x * gm.TILE_SIZE, y * gm.TILE_SIZE))
            
      gm.screen.blit(self._player, (32, 32))