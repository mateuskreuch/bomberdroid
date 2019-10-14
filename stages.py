import bombescii
from game_structs import Matrix

class Stage:
   def update(self, dt):        pass
   def draw(self):              pass
   def key_pressed(self, key):  pass
   def key_released(self, key): pass

class MainMenu(Stage):
   def __init__(self):
      self._bg = bombescii.new_image("gfx/tile_brick.png")

   def draw(self):
      bombescii.screen.blit(self._bg, (0, 0))

class Arena(Stage):
   def __init(self):
      self._tiles = Matrix(bombescii.MAP_SIZE.x, bombescii.MAP_SIZE.y)