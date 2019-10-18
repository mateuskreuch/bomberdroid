# this file is the entry point of the game

import pygame, gm, stages
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Bombescii")

gm.stage = stages.Arena()

clock   = pygame.time.Clock()
running = True

while running:
   dt = clock.tick(60)

   for event in pygame.event.get():
      if event.type == QUIT:
         running = False

      elif event.type == KEYDOWN:
         gm.stage.on_key_event(event.key, 1)
      
      elif event.type == KEYUP:
         gm.stage.on_key_event(event.key, -1)

   gm.stage.on_draw()
   gm.stage.on_update(dt / 1000)

   scaled = pygame.transform.scale(gm.screen, gm.window.get_size())
   gm.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()