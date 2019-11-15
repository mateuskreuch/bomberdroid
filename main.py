# This file is the entry point of the game.
#
# Some considerations:
#
# - Private variables are not defined with dunderscore (__) as name mangling
#   was implemented to avoid name clash when inheriting, not to allow private
#   members (https://docs.python.org/3/tutorial/classes.html#private-variables)
#
# - Fields are not encapsulated with getters and setters because if it comes
#   a time where it requires it, it can be done with Python's @property and
#   @xxx.setter

import pygame

pygame.init()
pygame.display.set_caption("BomberDroid")
pygame.mixer.init()

import lib, stages
from pygame.locals import *

pygame.display.set_icon(pygame.image.load(lib.DIR + "gfx/bomb_0.png"))

stages.current = stages.MainMenu()

clock   = pygame.time.Clock()
running = True

while running:
   dt = clock.tick(60)

   for event in pygame.event.get():
      if event.type == QUIT:
         running = False

      elif event.type == KEYDOWN:
         stages.current.on_key_event(event.key, 1)
      
      elif event.type == KEYUP:
         stages.current.on_key_event(event.key, 0)

   stages.current.on_draw(dt / 1000)
   stages.current.on_update(dt / 1000)

   scaled = pygame.transform.scale(lib.screen, lib.window.get_size())
   lib.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()