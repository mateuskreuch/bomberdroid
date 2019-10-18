# this file contains all tiles
# tiles are just data structures that contain visual info and some other details

import gm

class Tile:
   x = y = z = 0

   def on_update(self, dt):            pass
   def on_draw(self):                  pass
   def on_key_event(self, key, state): pass
   def on_move_attempt(self, tile):    return False

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   def move_to(self, x, y):
      dest = gm.stage.tmap.get(x, y, self.z)

      if dest is None or dest.on_move_attempt(self):
         gm.stage.tmap.move(self.x, self.y, self.z, x, y, self.z)
         self.x = x
         self.y = y

class TerrainTile(Tile):
   sprite = gm.new_image("gfx/tile_missing.png")

   def on_draw(self):
      gm.screen.blit(self.sprite, (self.x * gm.TILE_SIZE, self.y * gm.TILE_SIZE))

class TlGrass(TerrainTile): sprite = gm.new_image("gfx/tile_grass.png")
class TlBrick(TerrainTile): sprite = gm.new_image("gfx/tile_brick.png")

class TlPlayer(Tile):
   sprite = gm.new_image("gfx/player.png")

   def __init__(self, x, y, z, h_axis, v_axis):
      self.x = x
      self.y = y
      self.z = z
      self.h_axis = h_axis
      self.v_axis = v_axis
      self._last_moved_at = 0
   
   def on_update(self, dt):
      self._last_moved_at += dt

      if self._last_moved_at >= 0.1:
         dx = self.h_axis.value
         dy = self.v_axis.value

         if dx or dy:
            self._last_moved_at = 0
            self.move_to(self.x + dx, self.y + dy)

   def on_key_event(self, key, state):
      self.h_axis.react_to_key(key, state)
      self.v_axis.react_to_key(key, state)

   def on_draw(self):
      gm.screen.blit(self.sprite, (self.x * gm.TILE_SIZE, self.y * gm.TILE_SIZE))