# this file is the entry point of the game

import pygame, lib, stages
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Bombescii")

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
         stages.current.on_key_event(event.key, -1)

   stages.current.on_draw()
   stages.current.on_update(dt / 1000)

   scaled = pygame.transform.scale(lib.screen, lib.window.get_size())
   lib.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()