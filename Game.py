import pygame
import Enemy as en
import Player as pl
from random import randint

pygame.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

evils = [en.Enemy(randint(50, 550), randint(50, 550)),
         en.Enemy(randint(50, 550), randint(50, 550)),
         en.Enemy(randint(50, 550), randint(50, 550))]

Bullet_list = []

clock = pygame.time.Clock() # set FPS

running = True

while running: # mimicking game cycle
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()

    screen.fill((0, 0, 0)) # wipe screen
    
    for enemy in evils:
        
        enemy.movement() # call movement
        enemy.draw(screen) #draw new xy
        
        for bullet in Bullet_list:
            
            bullet.Bullet_vector()
    
        
    if pygame.time.get_ticks() % 60 == 0:
         
        for enemy in evils:
            b1 = en.Bullet(enemy.rect.centerx, enemy.rect.centery, pl.px, pl.py)
            Bullet_list.append(b1)

            
        if len(Bullet_list) > 50:
            Bullet_list = Bullet_list[(len(Bullet_list)//2) :]
    
    
    pygame.display.flip()
    
    clock.tick(60)