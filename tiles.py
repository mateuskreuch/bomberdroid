# this file contains all tiles
# tiles are just data structures that contain visual info and some other details

import gm

class Tile:
   sprite = gm.new_image("gfx/tile_missing.png")

class TlGrass(Tile):
   sprite = gm.new_image("gfx/tile_grass.png")

class TlBrick(Tile):
   sprite = gm.new_image("gfx/tile_brick.png")