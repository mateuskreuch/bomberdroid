# This file contains all the tiles.

import lib, stages, random
from lib import Image, Animation, Axis, Trigger
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
         stages.current.map.place(TlExplosion(self.x, self.y, self.z,
                                              leftover = self._pick_drop()))

      return False

   #

   def _pick_drop(self):
      chance = random.random()

      if   chance <= 0.20: return TlRuPass(-1, -1, -1)
      elif chance <= 0.55: return TlCoffee(-1, -1, -1)
      else:                return None

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
         tile.entering_bush.arm()
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

class TlCoffee(Tile):
   _sprite = Image("gfx/coffee.png")

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlPlayer):
         tile.bomb_cooldown *= 0.90
      
      return True

#-----------------------------------------------------------------------------#

class TlExplosion(Tile):
   def __init__(self, x, y, z, **params):
      super().__init__(x, y, z)

      self.leftover = params.get("leftover", None)
      
      self._sprite = Animation("gfx/explosion_%d.png", range(8))
      self._sprite.on_end = self._free

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
   _SOUND     = Sound("sfx/bomb.wav")

   #

   def __init__(self, x, y, z, **params):
      super().__init__(x, y, z)

      self._strength = params.get("strength", 2)
      self._in_bush  = params.get("in_bush", False)
      
      if self._in_bush:
         self._sprite = Image("gfx/bomb_bush.png")

      else:
         self._sprite = \
            Animation("gfx/bomb_%d.png", list(range(7))           + 
                                         list(reversed(range(7))) +
                                         list(range(7))           + 
                                         list(reversed(range(7))) +
                                         list(range(7))           )

      self._sprite.on_end = self.explode

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlExplosion):
         self.explode()
      
      elif isinstance(tile, TlCrate) and not self._in_bush:
         return self.move(self.x - tile.x, self.y - tile.y)
      
      elif isinstance(tile, TlPlayer) and self._in_bush:
         self.explode()
      
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

class TlPlayer(Tile):
   _SPRITES = {
      "a": {
         "normal": Animation("gfx/player_a_%d.png", (0, 1), 0.1),
         "nobomb": Animation("gfx/player_a_nobomb_%d.png", (0, 1), 0.1),
         "bush"  : Image("gfx/player_bush.png"),
      },
      "b": {
         "normal": Animation("gfx/player_b_%d.png", (0, 1), 0.1),
         "nobomb": Animation("gfx/player_b_nobomb_%d.png", (0, 1), 0.1),
         "bush"  : Image("gfx/player_bush.png"),
      }
   }
   _SLOWNESS    = 0.19

   #

   def __init__(self, x, y, z, id, axis, bomb_key):
      super().__init__(x, y, z)
      
      self.bomb_strength = 2
      self.bomb_cooldown = 1.75
      self.entering_bush = Trigger(False)

      self._axis        = axis
      self._bomb_key    = bomb_key
      self._id          = id

      self._time_not_moving  = self._SLOWNESS
      self._time_not_bombing = self.bomb_cooldown
      self._to_put_bomb      = Trigger(False)
      self._in_bush          = Trigger(False)

   #

   def on_overlapped(self, tile):
      if isinstance(tile, TlExplosion):
         tile.leftover = TlDeadPlayer(self.x, self.y, self.z, self._id)
         return True

      return False
   
   def on_update(self, dt):
      self._time_not_moving  += dt
      self._time_not_bombing += dt

      if  self._time_not_moving >= self._SLOWNESS \
      and self.move(self._axis.x, self._axis.y):
         self._time_not_moving = 0

         if  self._to_put_bomb.trigger()                 \
         and self._time_not_bombing >= self.bomb_cooldown:
            self._time_not_bombing = 0

            stages.current.map.place(
               TlBomb(self.x - self._axis.x, self.y - self._axis.y, self.z,
                      strength = self.bomb_strength,
                      in_bush  = self._in_bush.trigger()))

         elif self._in_bush.trigger():
            stages.current.map.place(TlBush(self.x - self._axis.x, 
                                            self.y - self._axis.y, 
                                            self.z))

         if self.entering_bush.trigger():
            self._in_bush.arm()

   def on_draw(self, dt):
      sprite = self._SPRITES[self._id]["normal"]

      if self._in_bush:
         sprite = self._SPRITES[self._id]["bush"]

      elif self._time_not_bombing < self.bomb_cooldown:
         sprite = self._SPRITES[self._id]["nobomb"]

      sprite.draw(self.x * lib.TILE_SIZE, self.y * lib.TILE_SIZE, dt)

   def on_key_event(self, key, state):
      self._axis.react_to_key(key, state)

      if key == self._bomb_key and state:
         self._to_put_bomb.arm()

#-----------------------------------------------------------------------------#

class TlDeadPlayer(Tile):
   _TIME_TO_RESTART = 1.5

   #

   def __init__(self, x, y, z, id):
      super().__init__(x, y, z)

      self._sprite = Animation("gfx/dying_%d.png", range(5))
      self._time_elapsed = 0
      self._id = id

      stages.current.decrease_health(id)

   #

   def on_update(self, dt):
      self._time_elapsed += dt

      if self._time_elapsed >= self._TIME_TO_RESTART:
         stages.current.player_lost(self._id)