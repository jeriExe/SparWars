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

youWin = False

youLose = False

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
    pygame.draw.rect(screen, ((0,0,0)), pygame.Rect(30, 30, 150, 10))
    pygame.draw.rect(screen, ((255,0,0)), pygame.Rect(30, 30, health, 10))
    
    font = pygame.font.SysFont('arial',  50)
    text = font.render(str(pl.killed), True, (255,255,255))
    textrect = text.get_rect()
    textrect.center = (925, 5)
    screen.blit(text, textrect.center)
    
    pygame.display.flip()


def menuScreen(screen, youWin, youLose):
    if youLose:
        font_size = 75
        msg = "YOU LOST, PLAY AGAIN?"
        fontColour = (255,12,32)
    elif youWin:
        font_size = 75
        msg = "YIPPIE! PLAY AGAIN?" 
        fontColour = (12,123,32)
    else:
        font_size = 100
        msg = "START"
        fontColour = (155,135,12)
    
    
    fontColour2 = (255, 232, 31)
    screen.fill((0,0,0))
    font = pygame.font.SysFont('timesnewroman', font_size)
    instructfont = pygame.font.SysFont('timesnewroman', 50)
    text = font.render(msg, True, (fontColour))
    textrect = text.get_rect()
    textrect.center = (screen_width//2 - textrect.centerx, 475 -textrect.centery)
    
    instruct = instructfont.render("USE WASD TO MOVE", True, (255,232,31))
    instructrect = instruct.get_rect()
    instructrect.center = (screen_width//2 - instructrect.centerx, 550 -instructrect.centery)
    
    title = pygame.image.load("Sparwars.png")
    titlerect = title.get_rect()
    titlerect.center = (screen_width//2 - titlerect.centerx, 225 -titlerect.centery)
    screen.blit(title, (titlerect.center))
    
    instruct2 = instructfont.render("RIGHT CLICK BUTTON TO START", True, (255,232,31))
    instruct2rect = instruct2.get_rect()
    instruct2rect.center = (screen_width//2 - instruct2rect.centerx, 600 -instruct2rect.centery)
    
    if textrect.collidepoint(pygame.mouse.get_pos()[0]-(text.get_width()//2), pygame.mouse.get_pos()[1]-(text.get_height()//2)):
        text = font.render(msg, True, (fontColour2))
        
        if pygame.mouse.get_pressed()[2]:
            global playing
            playing = True
    
    screen.blit(instruct2, instruct2rect.center)
    screen.blit(instruct, instructrect.center)
    screen.blit(text, textrect.center)
    pygame.display.flip()


def resetGame():
    play1.hp = 150
    pl.px = 100
    pl.py = 300
    pl.killed = 0
    en.evils.clear()
    en.Bullet_list.clear()
    pl.play_bullets.clear()


while running: # mimicking game cycle
    
    if play1.hp <= 0:
        youLose = True
        resetGame()
        playing = False
        
    elif pl.killed >= 5:
        youWin = True
        resetGame()
        playing = False
        
    if playing:
        youWin = False
        youLose = False
        gameDoStuff()
    else:
        menuScreen(screen, youWin, youLose)
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()
    
    clock.tick(60)

#meow


