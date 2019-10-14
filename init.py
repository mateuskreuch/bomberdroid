import pygame, bombescii, stages
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Bombescii")

bombescii.stage = stages.MainMenu()

clock   = pygame.time.Clock()
running = True

while running:
   dt = clock.tick(60)

   for event in pygame.event.get():
      if event.type == QUIT:
         running = False

      elif bombescii.stage is not None:
         if event.type == KEYDOWN:
            bombescii.stage.key_pressed(event.key)
         
         elif event.type == KEYUP:
            bombescii.stage.key_released(event.key)

   if bombescii.stage is not None:
      bombescii.stage.draw()
      bombescii.stage.update(dt / 1000)

   scaled = pygame.transform.scale(bombescii.screen, bombescii.window.get_size())
   bombescii.window.blit(scaled, (0, 0))
   pygame.display.flip()

pygame.quit()