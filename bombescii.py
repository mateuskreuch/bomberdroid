# this file is the entry point of the game
#
# some considerations:
#
# - private variables are not defined with dunderscore (__) as name mangling
#   was implemented to avoid name clash when inheriting, not to allow private
#   members (https://docs.python.org/3/tutorial/classes.html#private-variables)
#
# - fields are not encapsulated with getters and setters because if it comes
#   a time where it requires it, it can be done with python's @property and
#   @xxx.setter
#
# - the lack of comments is due to personal belief that a piece of code that 
#   needs explanation is not clear enough and should be cleaned, and that's 
#   where we put our effort instead

import pygame

pygame.init()
pygame.display.set_caption("Bombescii")
pygame.mixer.init()

import lib, stages
from pygame.locals import *

stages.current = stages.GrassArena()

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

   stages.current.on_draw()
   stages.current.on_update(dt / 1000)

   scaled = pygame.transform.scale(lib.screen, lib.window.get_size())
   lib.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()