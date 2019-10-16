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

      elif gm.stage is not None:
         if event.type == KEYDOWN:
            gm.stage.key_pressed(event.key)
         
         elif event.type == KEYUP:
            gm.stage.key_released(event.key)

   if gm.stage is not None:
      gm.stage.draw()
      gm.stage.update(dt / 1000)

   scaled = pygame.transform.scale(gm.screen, gm.window.get_size())
   gm.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()