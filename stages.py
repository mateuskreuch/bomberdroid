# This file contains the stages of the game.
# Stages are also commonly known as states or screens.

import random, lib
from pygame.locals import *
from lib           import TileMap, Image
from tiles         import *

#-----------------------------------------------------------------------------#

class Stage:
   def on_draw(self, dt):
      pass

   def on_key_event(self, key, state):
      pass

   def on_update(self, dt):
      pass

#-----------------------------------------------------------------------------#

class MainMenu(Stage):
   _BACKGROUND = Image("gfx/main_menu.png")
   
   #

   def on_draw(self, dt):
      self._BACKGROUND.draw(0, 0)

   def on_key_event(self, key, state):
      global current

      if key == K_RETURN and state == 0:
         current = GrassArena()

#-----------------------------------------------------------------------------#

class WinInfo(Stage):
   def __init__(self, id):
      if id == "a": self._background = Image("gfx/won_player_b.png")
      else:         self._background = Image("gfx/won_player_a.png")
   
   #

   def on_draw(self, dt):
      self._background.draw(0, 0)

   def on_key_event(self, key, state):
      global current

      if key == K_RETURN and state == 0:
         current = MainMenu()

#-----------------------------------------------------------------------------#

class Arena(Stage):
   _GEN_NOISE = 0.6

   #

   def __init__(self):
      self.on_generation()

      self._health_bar = {
         "a": Animation("gfx/health_bar_%d.png", range(4), float("inf")),
         "b": Animation("gfx/health_bar_%d.png", range(4), float("inf"))
      }

   #

   def on_generation(self):
      pass
   
   def on_draw(self, dt):
      for tile in self.map: tile.on_draw(dt)

      self._health_bar["a"].draw(6, 5, dt)
      self._health_bar["b"].draw(lib.SCREEN_SIZE_X - 37 - 4, 
                                 lib.SCREEN_SIZE_Y - 16 - 4, 
                                 dt)

   def on_key_event(self, key, state):
      for tile in self.map: tile.on_key_event(key, state)

   def on_update(self, dt):
      for tile in self.map: tile.on_update(dt)

   #

   def place_players(self):
      for x, y in ((1, 1), (2, 1), (1, 2)):
         self.map.remove(x                    , y                    , 1)
         self.map.remove(self.map.cols - 1 - x, self.map.rows - 1 - y, 1)

      self.map.place(
         TlPlayer(1, 1, 1,
                  "a",
                  Axis(K_w, K_a, K_s, K_d),
                  K_SPACE))

      self.map.place(
         TlPlayer(self.map.cols - 2, self.map.rows - 2, 1,
                  "b",
                  Axis(K_UP, K_LEFT, K_DOWN, K_RIGHT),
                  K_KP_ENTER))

   def player_lost(self, id):
      global current

      self.on_generation()

      if self._health_bar[id].at_frame == 3:
         current = WinInfo(id)

   def decrease_health(self, id):
      self._health_bar[id].at_frame += 1

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

#-----------------------------------------------------------------------------#

class GrassArena(Arena):
   _BREAKABLE_TILES = [
      TlBrick,
      TlBush,
      TlCrate
   ]

   #

   def on_generation(self):
      self.map = TileMap(lib.MAP_SIZE_X, lib.MAP_SIZE_Y, 2)

      for x, y, z in self.map.traverse():
         if z == 0:
            self.map.place(TlGrass(x, y, z))
         
         elif self._is_border_tile(x, y):
            self.map.place(TlConcrete(x, y, z))
      
         elif random.random() <= self._GEN_NOISE or self._is_lock_tile(x, y):
            self.map.place(random.choice(self._BREAKABLE_TILES)(x, y, z))
      
      self.place_players()
   
#-----------------------------------------------------------------------------#

current = None