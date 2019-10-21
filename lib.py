# this file contains data structures, wrappers and helper functions

import os, pygame

class Image:
   _cache = {}

   def __init__(self, path):
      try:
         self._surface = self._cache[path]
         
      except KeyError:
         self._surface = pygame.image.load(os.path.join(DIR, path)).convert_alpha()
         self._cache[path] = self._surface
   
   #

   def draw(self, x, y):
      screen.blit(self._surface, (x, y))

class Vector:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __mul__(self, other):
      try:    
         return Vector(self.x * other.x, self.y * other.y)

      except AttributeError: 
         return Vector(self.x * other, self.y * other)

   def __str__(self):
      return "v(%s, %s)" % (self.x, self.y)

   #
   
   def unpack(self):
      return (self.x, self.y)

class TileMap:
   def __init__(self, w, h, z):
      self.cols = w
      self.rows = h
      self.lyrs = z

      self._elms = [None] * (w*h*z)

   def __iter__(self):
      return (k for k in self._elms if k != None)

   #
   
   def get(self, x, y, z):
      return self._elms[z*self.cols*self.rows + y*self.cols + x]

   def is_inbounds(self, tile_or_x, y = None, z = 0):
      try:
         return tile_or_x.x >= 0        and \
                tile_or_x.y >= 0        and \
                tile_or_x.z >= 0        and \
                tile_or_x.x < self.cols and \
                tile_or_x.y < self.rows and \
                tile_or_x.z < self.lyrs
      
      except AttributeError:
         return tile_or_x >= 0        and \
                y         >= 0        and \
                z         >= 0        and \
                tile_or_x < self.cols and \
                y         < self.rows and \
                z         < self.lyrs

   def place(self, tile):
      self._elms[tile.z*self.cols*self.rows +
                 tile.y*self.cols           +
                 tile.x                     ] = tile

   def place_if_possible(self, tile):
      dest = self.get(tile.x, tile.y, tile.z)

      if dest is None or dest.can_be_replaced_by(tile):
         self.place(tile)

   def remove(self, tile_or_x, y = None, z = None):
      try:
         self._elms[tile_or_x.z*self.cols*self.rows +
                    tile_or_x.y*self.cols           +
                    tile_or_x.x                     ] = None

      except AttributeError:
         self._elms[z*self.cols*self.rows +
                    y*self.cols           +
                    tile_or_x             ] = None

   def traverse(self):
      return ((x, y, z) for z in range(self.lyrs) 
                        for y in range(self.rows) 
                        for x in range(self.cols))

class Axis:
   def __init__(self, *keys):
      self.value = 0

      self._counter = [0, 0]
      self._keys    = {key: sign for key, sign in keys}

   #

   def react_to_key(self, key, state):
      if key in self._keys:
         if   self._keys[key] > 0: self._counter[0] += state
         elif self._keys[key] < 0: self._counter[1] += state

         if   self._counter[0] and not self._counter[1]: self.value =  1
         elif self._counter[1] and not self._counter[0]: self.value = -1
         else                                          : self.value =  0

DIR = os.path.abspath("")

PIXEL_SCALE = 2
TILE_SIZE   = 32

MAP_SIZE    = Vector(2*6 + 3, 2*5 + 3)
SCREEN_SIZE = MAP_SIZE * TILE_SIZE
WINDOW_SIZE = SCREEN_SIZE * PIXEL_SCALE

window = pygame.display.set_mode(WINDOW_SIZE.unpack())
screen = pygame.Surface(SCREEN_SIZE.unpack())

"""
class Matrix:
   def __init__(self, w, h):
      self.cols = w
      self.rows = h
      
      self._elms = [None] * (w * h)

   def __iter__(self):
      return (
         (x, y, self.get(x, y))
         for y in range(self.rows)
         for x in range(self.cols))

   #
   
   def get(self, x, y):
      return self._elms[y * self.cols + x]

   def set(self, x, y, value = None):
      self._elms[y * self.cols + x] = value

   def is_inside(self, x, y):
      return x >= 0 and y >= 0 and x < self.cols and y < self.rows 
"""