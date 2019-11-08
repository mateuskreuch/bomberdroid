# This file contains general classes, data structures and constants

import pygame, inspect

#-----------------------------------------------------------------------------#

class Image:
   _cache = {}

   #

   def __init__(self, path):
      self._surface = self._load_or_create_sprite(path)
   
   #

   def draw(self, x, y, dt = None):
      screen.blit(self._surface, (x, y))

   #

   def _load_or_create_sprite(self, path):
      if path not in self._cache:
         self._cache[path] = pygame.image.load(DIR + path).convert_alpha()

      return self._cache[path]

#-----------------------------------------------------------------------------#

class Animation(Image):
   _SECONDS_PER_FRAME = 0.05

   #

   def __init__(self, paths):
      self._time_counter = 0
      self._at_frame     = 0
      self._surfaces     = []

      for path in paths:
         self._surfaces.append(self._load_or_create_sprite(path))

      self._frame_amount = len(self._surfaces)

   #

   def on_end(self): 
      pass

   #

   def draw(self, x, y, dt):
      self._time_counter += dt

      if self._time_counter >= self._SECONDS_PER_FRAME:
         self._time_counter = 0
         self._at_frame += 1

         if self._at_frame >= self._frame_amount - 1:
            self.on_end()

      screen.blit(self._surfaces[self._at_frame % self._frame_amount], (x, y))

#-----------------------------------------------------------------------------#

class TileMap:
   def __init__(self, w, h, z):
      self.cols = w
      self.rows = h
      self.lyrs = z

      self._elms = [None] * (w*h*z)

   #

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

   def place_attempt(self, tile):
      dest = self.get(tile.x, tile.y, tile.z)

      if dest is None or dest.on_overlapped(tile):
         self.place(tile)
         return True
      
      return False

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

#-----------------------------------------------------------------------------#

class Trigger:
   def __init__(self, default):
      self._state = default

   #

   def __eq__(self, other):
      return self._state == other
   
   def __bool__(self):
      return self._state
   
   #

   def trigger(self):
      if self._state:
         self._state = False
         return True

      return False

   def setup(self, value):
      self._state = value

#-----------------------------------------------------------------------------#

class Axis:
   def __init__(self, up, left, down, right):
      self.x = self.y = 0

      self._u = up
      self._l = left
      self._d = down
      self._r = right
      
      self._u_pressed = self._l_pressed = self._d_pressed = self._r_pressed = 0

   #

   def react_to_key(self, key, state):
      if   key == self._u: self._u_pressed = state
      elif key == self._l: self._l_pressed = state
      elif key == self._d: self._d_pressed = state
      elif key == self._r: self._r_pressed = state

      keys_pressed = self._u_pressed + self._l_pressed + \
                     self._d_pressed + self._r_pressed

      if keys_pressed == 0:
         self.x = self.y = 0

      elif keys_pressed == 1:
         if   self._u_pressed: self.x, self.y =  0, -1
         elif self._l_pressed: self.x, self.y = -1,  0
         elif self._d_pressed: self.x, self.y =  0,  1
         elif self._r_pressed: self.x, self.y =  1,  0

#-----------------------------------------------------------------------------#

DIR = inspect.getfile(inspect.currentframe()) \
      .replace("\\", "/")                     \
      .rsplit("/", 1)[0]                      \
      + "/"

PIXEL_SCALE   = 2
TILE_SIZE     = 32
MAP_SIZE_Y    = 2*5 + 3
MAP_SIZE_X    = 2*6 + 3
SCREEN_SIZE_X = MAP_SIZE_X * TILE_SIZE
SCREEN_SIZE_Y = MAP_SIZE_Y * TILE_SIZE
WINDOW_SIZE_X = SCREEN_SIZE_X * PIXEL_SCALE
WINDOW_SIZE_Y = SCREEN_SIZE_Y * PIXEL_SCALE

window = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
screen = pygame.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))