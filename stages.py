# this file contains the stages of the game
# stages are also commonly known as states or screens, and is basically a piece
# of the game

import random
from pygame.locals import *
from lib           import TileMap, Axis
from tiles         import *

class Stage:
   def on_draw(self):                  pass
   def on_key_event(self, key, state): pass
   def on_update(self, dt):            pass

class MainMenu(Stage):
   pass

class Arena(Stage):
   def __init__(self):
      self.map = TileMap(lib.MAP_SIZE.x, lib.MAP_SIZE.y, 2)

      for x, y, z in self.map.traverse():
         if z == 0:
            self.map.place(TlGrass(x, y, z))
         
         elif x == 0                  or y == 0                  or \
              x == self.map.cols - 1 or y == self.map.rows - 1 or \
              (x % 2 == 0 and y % 2 == 0):
            self.map.place(TlConcrete(x, y, z))
      
         elif random.random() <= 0.1:
            self.map.place(TlBomb(x, y, z))
            

      self.map.place(
         TlPlayer(1, 1, 1,
            Axis((K_d, 1), (K_a, -1)),
            Axis((K_s, 1), (K_w, -1))))

      self.map.place(
         TlPlayer(self.map.cols - 2, self.map.rows - 2, 1,
            Axis((K_RIGHT, 1), (K_LEFT, -1)),
            Axis((K_DOWN, 1), (K_UP, -1))))

   #
   
   def on_draw(self):
      for tile in self.map: tile.on_draw()

   def on_key_event(self, key, state):
      for tile in self.map: tile.on_key_event(key, state)

   def on_update(self, dt):
      for tile in self.map: tile.on_update(dt)

current = None