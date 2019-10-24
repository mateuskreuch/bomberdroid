# this file contains all tiles

import lib, stages, random
from lib import Image, AnimatedImage, Axis

class Tile:
   _sprite = Image("gfx/missing.png")
   x = y = z = 0

   #

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   #

   def on_update(self, dt)           : pass
   def on_key_event(self, key, state): pass
   def on_destroy_attempt(self, tile): return False
   def on_draw(self):
      self._sprite.draw(self.x * lib.TILE_SIZE, self.y * lib.TILE_SIZE)

   #

   def move_to(self, x, y):
      dest = stages.current.map.get(x, y, self.z)

      if dest is None or dest.on_destroy_attempt(self):
         stages.current.map.remove(self)
         self.x = x
         self.y = y
         stages.current.map.place(self)

         return True
      
      return False

class BreakableTile(Tile):
   def on_destroy_attempt(self, tile):
      if isinstance(tile, TlExplosion):
         stages.current.map.remove(self)
         stages.current.map.place(TlBroken(self.x, self.y, self.z))

      return False

class TlGrass(Tile):
   _sprite = Image("gfx/grass.png")

class TlConcrete(Tile):
   _sprite = Image("gfx/concrete.png")

class TlBrick(BreakableTile):
   _sprite = Image("gfx/brick.png")

class TlBush(BreakableTile):
   _sprite = Image("gfx/bush.png")

class TlExplosion(Tile):
   def __init__(self, x, y, z):
      super().__init__(x, y, z)

      self._sprite = AnimatedImage(*("gfx/explosion_%d.png" % k for k in range(12)))

   #

   def on_update(self, dt):
      self._sprite.update(dt)

      if self._sprite.get_completion() >= 1:
         stages.current.map.remove(self)

   def on_destroy_attempt(self, tile):
      return True
   
class TlBomb(Tile):
   def __init__(self, x, y, z, strength = 2):
      super().__init__(x, y, z)

      a = ["gfx/bomb_%d.png" % k for k in range(8)]
      b = list(reversed(a))

      self._sprite   = AnimatedImage(*(a + b + a + b + a))
      self._strength = strength

   #

   def on_update(self, dt):
      self._sprite.update(dt)

      if self._sprite.get_completion() >= 1:
         self.explode()

   def on_destroy_attempt(self, tile):
      if isinstance(tile, TlExplosion):
         self.explode()
      
      return False

   #

   def explode(self):
      stages.current.map.remove(self)
      stages.current.map.place(TlExplosion(self.x, self.y, self.z))

      for k in (-1, 1):
         for x in range(1, self._strength + 1):
            if not stages.current.map.place_if_possible(TlExplosion(self.x + x*k, self.y, self.z)):
               break

         for y in range(1, self._strength + 1):
            if not stages.current.map.place_if_possible(TlExplosion(self.x, self.y + y*k, self.z)):
               break

class TlRuPass(Tile):
   _sprite = Image("gfx/ru_pass.png")

   #

   def on_destroy_attempt(self, tile):
      return True

class TlBroken(Tile):
   DROP_CHANCE = 0.5
   DROPS = [
      TlRuPass
   ]

   #

   def __init__(self, x, y, z):
      super().__init__(x, y, z)

      self._sprite = AnimatedImage(*("gfx/broken_%d.png" % k for k in range(4)))

   #
   
   def on_update(self, dt):
      self._sprite.update(dt)

      if self._sprite.get_completion() >= 1:
         stages.current.map.remove(self)

         if random.random() <= self.DROP_CHANCE:
            drop = random.choice(self.DROPS)
            stages.current.map.place(drop(self.x, self.y, self.z))

class TlPlayer(Tile):
   def __init__(self, x, y, z, img, h_axis, v_axis, bomb_key):
      self.x      = x
      self.y      = y
      self.z      = z
      self._h_axis = h_axis
      self._v_axis = v_axis
      self._bomb_key = bomb_key
      self._sprite = img

      self._last_moved_at = 0
      self._placed_bomb = False

   #

   def on_destroy_attempt(self, tile):
      if isinstance(tile, TlExplosion):
         return True
      
      return False
   
   def on_update(self, dt):
      self._last_moved_at += dt

      if self._last_moved_at >= 0.2:
         dx = self._h_axis.value
         dy = self._v_axis.value

         if dx or dy:
            self._last_moved_at = 0

            if self.move_to(self.x + dx, self.y + dy) and self._placed_bomb:
               stages.current.map.place(TlBomb(self.x - dx, self.y - dy, self.z, 2))
               self._placed_bomb = False

   def on_key_event(self, key, state):
      self._h_axis.react_to_key(key, state)
      self._v_axis.react_to_key(key, state)

      if key == self._bomb_key and state > 0:
         self._placed_bomb = True