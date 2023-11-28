import pygame
import Enemy as en
import Player as pl
from random import randint
pygame.init() #init the pygame mod

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height)) #set resolution 

clock = pygame.time.Clock() # set FPS

running = True #bool for while loop

play1 = pl.Player()

playing = False

def gameDoStuff():
    screen.fill((59, 21, 28)) # wipe screen
    
    if len(en.evils) < 3:
        if pygame.time.get_ticks() % 100 == 0:    
            respawn = en.Enemy(randint(50, 950), randint(50, 650), randint(3,6))
            en.evils.append(respawn)
    
    for enemy in en.evils:
        
        enemy.movement(pl.px, pl.py) # call movement
        enemy.update(screen, play1) #draw new xy
        
        for bullet in en.Bullet_list:
            bullet.Bullet_vector(screen)
        
    if pygame.time.get_ticks() %60 == 0:
         
        for enemy in en.evils:
            b1 = en.Bullet(enemy.rect.centerx, enemy.rect.centery, pl.px, pl.py)
            en.Bullet_list.append(b1)  
    
    
    keys = pygame.key.get_pressed()
    rot_image, rot_image_rect, angle = play1.rotate()

    pl.px, pl.py = play1.move(pl.px, pl.py, keys)
    for pbullet in pl.play_bullets:
        pbullet.bullet_move()
        pbullet.draw(screen)
    play1.draw_cursor(screen)
    screen.blit(rot_image, rot_image_rect)
    
    play1.collide()
    
    health = int(play1.hp)
    pygame.draw.rect(screen, ((0,0,0)), pygame.Rect(30, 30, 200, 10))
    pygame.draw.rect(screen, ((255,0,0)), pygame.Rect(30, 30, health, 10))
    
    font = pygame.font.SysFont('arial',  50)
    text = font.render(str(pl.killed), True, (255,255,255))
    textrect = text.get_rect()
    textrect.center = (925, 5)
    screen.blit(text, textrect.center)
    
    pygame.display.flip()


def menuScreen(screen):
    fontColour = (12,123,32)
    fontColour2 = (24, 246, 64)
    screen.fill((34,34,34))
    font = pygame.font.SysFont('timesnewroman', 200)
    text = font.render('Start', True, (fontColour))
    textrect = text.get_rect()
    textrect.center = (screen_width//2 - textrect.centerx, screen_height//2 -textrect.centery)
    
    if textrect.collidepoint(pygame.mouse.get_pos()[0]-(text.get_width()//2), pygame.mouse.get_pos()[1]-(text.get_height()//2)):
        text = font.render('Start', True, (fontColour2))
        
        if pygame.mouse.get_pressed()[0]:
            global playing
            playing = True
    
    
    screen.blit(text, textrect.center)
    pygame.display.flip()

while running: # mimicking game cycle
    
    if playing:
        gameDoStuff()
    else:
        menuScreen(screen)
    
    if play1.hp <= 0:
        playing = False
        
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()

    
    
    
    
    clock.tick(60)

#meow


