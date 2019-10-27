# this file contains all tiles

import lib, stages, random
from lib import Image, Animation, Axis

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
      if x == self.x and y == self.y:
         return False

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
         stages.current.map.place(TlBroken(self.x, self.y, self.z))

      return False
   
   #

class TlGrass(Tile):
   _sprite = Image("gfx/grass.png")

class TlConcrete(Tile):
   _sprite = Image("gfx/concrete.png")

class TlBrick(BreakableTile):
   _sprite = Image("gfx/brick.png")

class TlBush(BreakableTile):
   _sprite = Image("gfx/bush.png")

   #

   def on_destroy_attempt(self, tile):
      super().on_destroy_attempt(tile)

      if isinstance(tile, TlPlayer):
         tile.hide_in_bush()
         return True
      
      return False

class TlCrate(BreakableTile):
   _sprite = Image("gfx/crate.png")

   def on_destroy_attempt(self, tile):
      super().on_destroy_attempt(tile)

      if isinstance(tile, (TlPlayer, TlCrate)):
         dx = self.x - tile.x
         dy = self.y - tile.y

         return self.move_to(self.x + dx, self.y + dy)
      
      return False

class TlExplosion(Tile):
   def __init__(self, x, y, z):
      super().__init__(x, y, z)

      self._sprite = Animation("gfx/explosion_%d.png" % k for k in range(12))

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

      a = ["gfx/bomb_%d.png" % k for k in range(7)]
      z = list(reversed(a))

      self._sprite   = Animation(a + z + a + z + a)
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
      stages.current.map.place(TlExplosion(self.x, self.y, self.z))

      for ix, iy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
         for i in range(1, self._strength + 1):
            if not stages.current.map.place_attempt(
            TlExplosion(self.x + i*ix, self.y + i*iy, self.z)):
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

      self._sprite = Animation("gfx/broken_%d.png" % k for k in range(4))

   #
   
   def on_update(self, dt):
      self._sprite.update(dt)

      if self._sprite.get_completion() >= 1:
         stages.current.map.remove(self)

         if random.random() <= self.DROP_CHANCE:
            drop = random.choice(self.DROPS)
            stages.current.map.place(drop(self.x, self.y, self.z))

class TlPlayer(Tile):
   PLAYER_BUSH_SPRITE = Image("gfx/player_bush.png")
   SLOWNESS = 0.18

   #

   def __init__(self, x, y, z, img, axis, bomb_key):
      self.x = x
      self.y = y
      self.z = z
      
      self.bomb_strength = 2

      self._axis          = axis
      self._bomb_key      = bomb_key
      self._sprite        = img

      self._last_moved_at = 0
      self._to_put_bomb   = False
      self._in_bush       = 0

   #

   def on_destroy_attempt(self, tile):
      if isinstance(tile, TlExplosion):
         return True

      elif isinstance(tile, TlCrate):
         dx = self.x - tile.x
         dy = self.y - tile.y

         self.move_to(self.x + dx, self.y + dy)
         return True
      
      return False
   
   def on_update(self, dt):
      self._sprite.update(dt)

      self._last_moved_at += dt

      was_on_bush = self._in_bush

      if  self._last_moved_at >= self.SLOWNESS                              \
      and self.move_to(self.x + self._axis.dir_x, self.y + self._axis.dir_y):
         self._last_moved_at = 0

         if was_on_bush:
            self._in_bush -= 1

            stages.current.map.place(TlBush(self.x - self._axis.dir_x, 
                                            self.y - self._axis.dir_y, 
                                            self.z))
         
         if self._to_put_bomb:
            self._to_put_bomb = False

            stages.current.map.place(TlBomb(self.x - self._axis.dir_x,
                                            self.y - self._axis.dir_y,
                                            self.z,
                                            self.bomb_strength))

   def on_draw(self):
      if self._in_bush:
         self.PLAYER_BUSH_SPRITE.draw(self.x * lib.TILE_SIZE, self.y * lib.TILE_SIZE)

      else:
         super().on_draw()

   def on_key_event(self, key, state):
      self._axis.react_to_key(key, state)

      if key == self._bomb_key and state and not self._in_bush:
         self._to_put_bomb = True

   #

   def hide_in_bush(self):
      self._in_bush += 1