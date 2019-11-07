# This file contains all the tiles.

import lib, stages, random
from lib import Image, Animation, Axis
from pygame.mixer import Sound

#-----------------------------------------------------------------------------#

class Tile:
   _sprite = Image("gfx/missing.png")
   x = y = z = 0

   #

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   #

   def on_update(self, dt): 
      pass

   def on_key_event(self, key, state): 
      pass

   def on_overlapped(self, tile):
      return False

   def on_draw(self, dt):
      self._sprite.draw(self.x * lib.TILE_SIZE, self.y * lib.TILE_SIZE, dt)

   #

   def move(self, dx, dy):
      if dx == 0 and dy == 0:
         return False

      dx += self.x
      dy += self.y

      dest = stages.current.map.get(dx, dy, self.z)

      if dest is None or dest.on_overlapped(self):
         stages.current.map.remove(self)
         self.x = dx
         self.y = dy
         stages.current.map.place(self)

         return True
      
      return False

#-----------------------------------------------------------------------------#

class BreakableTile(Tile):
   def on_overlapped(self, tile):
      if isinstance(tile, TlExplosion):
         stages.current.map.place(TlExplosion(self.x, self.y, self.z)
                                     .with_leftover(self._pick_drop()))

      return False

   #

   def _pick_drop(self):
      chance = random.random()

      if chance <= 0.5: return TlRuPass(-1, -1, -1)
      else:             return None

#-----------------------------------------------------------------------------#

class TlGrass(Tile):
   _sprite = Image("gfx/grass.png")

#-----------------------------------------------------------------------------#

class TlConcrete(Tile):
   _sprite = Image("gfx/concrete.png")

#-----------------------------------------------------------------------------#

class TlBrick(BreakableTile):
   _sprite = Image("gfx/brick.png")

#-----------------------------------------------------------------------------#

class TlBush(BreakableTile):
   _sprite = Image("gfx/bush.png")

   #

   def on_overlapped(self, tile):
      super().on_overlapped(tile)

      if isinstance(tile, TlPlayer):
         tile.hide_in_bush()
         return True

      return False

#-----------------------------------------------------------------------------#

class TlCrate(BreakableTile):
   _sprite = Image("gfx/crate.png")

   #

   def on_overlapped(self, tile):
      super().on_overlapped(tile)

      if isinstance(tile, (TlPlayer, TlCrate)):
         return self.move(self.x - tile.x, self.y - tile.y)
      
      return False

#-----------------------------------------------------------------------------#

class TlRuPass(Tile):
   _sprite = Image("gfx/ru_pass.png")

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlPlayer):
         tile.bomb_strength += 1
      
      return True

#-----------------------------------------------------------------------------#

class TlExplosion(Tile):
   def __init__(self, x, y, z):
      super().__init__(x, y, z)

      self.leftover = None
      
      self._sprite = Animation("gfx/explosion_%d.png" % k for k in range(8))
      self._sprite.on_end = self._free

   def with_leftover(self, leftover):
      self.leftover = leftover
      return self

   #

   def _free(self):
      stages.current.map.remove(self)

      if self.leftover is not None:
         self.leftover.x = self.x
         self.leftover.y = self.y
         self.leftover.z = self.z

         stages.current.map.place(self.leftover)

#-----------------------------------------------------------------------------#

class TlBomb(Tile):
   _SOUND = Sound("sfx/bomb.wav")

   #

   def __init__(self, x, y, z):
      super().__init__(x, y, z)

      self._strength = 2
      
      self._sprite = \
         Animation("gfx/bomb_%d.png" % k for k in list(range(7))           + 
                                                  list(reversed(range(7))) +
                                                  list(range(7))           + 
                                                  list(reversed(range(7))) +
                                                  list(range(7))           )

      self._sprite.on_end = self.explode

   def with_strength(self, strength):
      self._strength = strength
      return self

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlExplosion):
         self.explode()
      
      elif isinstance(tile, TlCrate):
         return self.move(self.x - tile.x, self.y - tile.y)
      
      return False

   #

   def explode(self):
      self._SOUND.play()

      stages.current.map.place(TlExplosion(self.x, self.y, self.z))

      for ix, iy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
         for i in range(1, self._strength + 1):
            if not stages.current.map.place_attempt(
            TlExplosion(self.x + i*ix, self.y + i*iy, self.z)):
               break

#-----------------------------------------------------------------------------#

class TlBombBush(Tile):
   _sprite = Image("gfx/bomb_bush.png")

   #

   def __init__(self, x, y, z):
      super().__init__(x, y, z)

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlPlayer):
         tile.kill()
         return True

      return False

#-----------------------------------------------------------------------------#

class TlPlayer(Tile):
   _BUSH_SPRITE = Image("gfx/player_bush.png")
   _SLOWNESS = 0.18

   #

   def __init__(self, x, y, z, img, axis, bomb_key):
      super().__init__(x, y, z)
      
      self.bomb_strength = 2

      self._axis          = axis
      self._bomb_key      = bomb_key
      self._sprite        = img

      self._last_moved_at = 0
      self._to_put_bomb   = False
      self._in_bush       = 0

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlExplosion):
         self.kill()
         tile.leftover = self
         return True

      return False
   
   def on_update(self, dt):
      self._last_moved_at += dt

      was_on_bush = self._in_bush

      if  self._last_moved_at >= self._SLOWNESS \
      and self.move(self._axis.x, self._axis.y) :
         self._last_moved_at = 0

         if was_on_bush:
            self._in_bush -= 1

            stages.current.map.place(TlBush(self.x - self._axis.x, 
                                            self.y - self._axis.y, 
                                            self.z))
         
         if self._to_put_bomb:
            self._to_put_bomb = False

            stages.current.map.place(TlBomb(self.x - self._axis.x,
                                            self.y - self._axis.y,
                                            self.z)
                                        .with_strength(self.bomb_strength))

   def on_draw(self, dt):
      if self._in_bush:
         self._BUSH_SPRITE.draw(self.x * lib.TILE_SIZE, self.y * lib.TILE_SIZE)

      else:
         super().on_draw(dt)

   def on_key_event(self, key, state):
      self._axis.react_to_key(key, state)

      if key == self._bomb_key and state and not self._in_bush:
         self._to_put_bomb = True

   #

   def kill(self):
      self._sprite = Animation("gfx/dying_%d.png" % k for k in range(5))

   def hide_in_bush(self):
      self._in_bush += 1