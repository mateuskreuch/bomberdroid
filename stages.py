# this file contains the stages of the game
# stages are also commonly known as states or screens, and is basically a piece
# of the game

import gm
from pygame.locals import *
from structs import *
from tiles import *

class Stage:
   def on_update(self, dt):            pass
   def on_draw(self):                  pass
   def on_key_event(self, key, state): pass

class MainMenu(Stage):
   pass

class Arena(Stage):
   def __init__(self):
      self.tmap = Tensor(gm.MAP_SIZE.x, gm.MAP_SIZE.y, 2)

      for x, y, z, _ in self.tmap:
         if z == 0:
            self.tmap.set(x, y, z, TlGrass(x, y, z))
         
         elif x == 0 or y == 0 or x == self.tmap.cols - 1 or y == self.tmap.rows - 1 or (x % 2 == 0 and y % 2 == 0):
            self.tmap.set(x, y, z, TlBrick(x, y, z))

      self.tmap.set(1, 1, 1, TlPlayer(1, 1, 1,
         Axis((K_d, 1), (K_a, -1)),
         Axis((K_s, 1), (K_w, -1))
         ))

   def on_update(self, dt):
      for x, y, z, tile in self.tmap:
         if tile is not None:
            tile.on_update(dt)
   
   def on_key_event(self, key, state):
      for x, y, z, tile in self.tmap:
         if tile is not None:
            tile.on_key_event(key, state)

   def on_draw(self):
      for x, y, z, tile in self.tmap:
         if tile is not None:
            tile.on_draw()