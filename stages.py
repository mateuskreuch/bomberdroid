# this file contains the stages of the game
# stages are also commonly known as states or screens

import random
from pygame.locals import *
from lib           import TileMap
from tiles         import *

#-----------------------------------------------------------------------------#

class Stage:
   def on_draw(self, dt):              pass
   def on_key_event(self, key, state): pass
   def on_update(self, dt):            pass

#-----------------------------------------------------------------------------#

class MainMenu(Stage):
   pass

#-----------------------------------------------------------------------------#

class Arena(Stage):
   _GEN_NOISE = 0.6

   #

   def __init__(self):
      self.map = TileMap(lib.MAP_SIZE_X, lib.MAP_SIZE_Y, 2)

      self.on_generation()
      self._place_players()

   #

   def on_generation(self): pass
   
   def on_draw(self, dt):
      for tile in self.map: tile.on_draw(dt)

   def on_key_event(self, key, state):
      for tile in self.map: tile.on_key_event(key, state)

   def on_update(self, dt):
      for tile in self.map: tile.on_update(dt)

   #

   def _is_border_tile(self, x, y):
      return x == 0                 or y == 0                 or \
             x == self.map.cols - 1 or y == self.map.rows - 1 or \
             (x % 2 == 0 and y % 2 == 0)

   def _is_lock_tile(self, x, y):
      return (x == 3                 and y == 1                ) or \
             (x == 1                 and y == 3                ) or \
             (x == self.map.cols - 4 and y == self.map.rows - 2) or \
             (x == self.map.cols - 2 and y == self.map.rows - 4)

   def _place_players(self):
      for x, y in ((1, 1), (2, 1), (1, 2)):
         self.map.remove(x                    , y                    , 1)
         self.map.remove(self.map.cols - 1 - x, self.map.rows - 1 - y, 1)

      self.map.place(
         TlPlayer(1, 1, 1,
                  Animation("gfx/player_a_%d.png" % k for k in range(2)),
                  Axis(K_w, K_a, K_s, K_d),
                  K_v))

      self.map.place(
         TlPlayer(self.map.cols - 2, self.map.rows - 2, 1,
                  Animation("gfx/player_b_%d.png" % k for k in range(2)),
                  Axis(K_UP, K_LEFT, K_DOWN, K_RIGHT),
                  K_KP3))

#-----------------------------------------------------------------------------#

class GrassArena(Arena):
   _BREAKABLE_TILES = [
      TlBrick,
      TlBush,
      TlCrate
   ]

   #

   def on_generation(self):
      for x, y, z in self.map.traverse():
         if z == 0:
            self.map.place(TlGrass(x, y, z))
         
         elif self._is_border_tile(x, y) and not y == self.map.rows//2:
            self.map.place(TlConcrete(x, y, z))
      
         elif random.random() <= self._GEN_NOISE or self._is_lock_tile(x, y):
            self.map.place(random.choice(self._BREAKABLE_TILES)(x, y, z))

#-----------------------------------------------------------------------------#

current = None