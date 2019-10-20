# this file contains all tiles

import gm

class Tile:
   sprite = gm.new_image("gfx/tile_missing.png")
   x = y = z = 0

   #

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   #

   def on_update(self, dt)           : pass
   def on_key_event(self, key, state): pass
   def on_move_attempt(self, tile)   : pass
   def on_draw(self):
      gm.screen.blit(self.sprite, (self.x * gm.TILE_SIZE, self.y * gm.TILE_SIZE))

   #

   def move_to(self, x, y):
      dest = gm.stage.tmap.get(x, y, self.z)

      if dest is not None:
         dest.on_move_attempt(self)

         dest = gm.stage.tmap.get(x, y, self.z)

      if dest is None or dest.can_be_overriden_by(self):
         gm.stage.tmap.remove(self)
         self.x = x
         self.y = y
         gm.stage.tmap.place(self)

   def can_be_overriden_by(self, tile):
      return False

class TlGrass(Tile): 
   sprite = gm.new_image("gfx/tile_grass.png")

class TlBrick(Tile):
   sprite = gm.new_image("gfx/tile_brick.png")

class TlPlayer(Tile):
   sprite = gm.new_image("gfx/player.png")

   #

   def __init__(self, x, y, z, h_axis, v_axis):
      self.x      = x
      self.y      = y
      self.z      = z
      self.h_axis = h_axis
      self.v_axis = v_axis

      self._last_moved_at = 0

   #
   
   def on_update(self, dt):
      self._last_moved_at += dt

      if self._last_moved_at >= 0.2:
         dx = self.h_axis.value
         dy = self.v_axis.value

         if dx or dy:
            self._last_moved_at = 0
            self.move_to(self.x + dx, self.y + dy)

   def on_key_event(self, key, state):
      self.h_axis.react_to_key(key, state)
      self.v_axis.react_to_key(key, state)