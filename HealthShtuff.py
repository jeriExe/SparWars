import pygame
import math
import Enemy as en
import Player as pl

pygame.init()

play = pl.Player()
screen = pygame.display.set_mode((1000, 700))

running = True

def player_health_bar(screen):
    health = int(play.hp)
    print(health)
    pygame.draw.rect(screen, ((255,0,0)), pygame.Rect(30, 30, health, 10))
    
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
    player_health_bar(screen)
    pygame.display.flip()
