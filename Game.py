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

play1 = pl.Player() #create instance of player 

playing = False #playing bool that triggers game starting initialized to false
                #you win/ lose also set to False by default as they trigger end screens
youWin = False 

youLose = False 

pygame.mixer.music.load("Act_DS_Escape.wav") #loads the main game soundtrack

def gameDoStuff(): #function that contains main game sequence/updates
    screen.fill((0, 0, 0)) # wipe screens
    
    background() #generates the starfield
    
    if len(en.evils) < 5: #limits number of enemies on screen at once
        if pygame.time.get_ticks() % 100 == 0:    #rate at which enemies can spawn
            respawn = en.Enemy(randint(50, 500), randint(50, 650), randint(3,5)) #generates random position and spawns enemy there
            en.evils.append(respawn)
            spawn2 = en.Enemy(randint(550, 950), randint(50, 650), randint(3,5)) #spawns enemy in a different random range
            en.evils.append(spawn2)
            
    
    for enemy in en.evils: #updates for each enemy on screen
        enemy.movement(play1.px, play1.py) # call movement
        enemy.update(screen, play1) #draw new xy
        
    for bullet in en.Bullet_list: #updates each bullet position independently
        bullet.Bullet_vector(screen)
        
    if pygame.time.get_ticks() %60 == 0:  #rate at which enemy bullets automatically fire
         
        for enemy in en.evils:  #adds a bullet at the enemy position and adds it to list of total bullets
            b1 = en.Bullet(enemy.rect.centerx, enemy.rect.centery, play1.px, play1.py)
            en.Bullet_list.append(b1)  
    
    
    keys = pygame.key.get_pressed() #continuous check, determines which keys are being pressed at any time. gets passed to player
    rot_image, rot_image_rect = play1.rotate()

    play1.px, play1.py = play1.move(keys)
    
    for pbullet in pl.play_bullets:
        pbullet.bullet_move()
        pbullet.draw(screen)
    play1.draw_cursor(screen)
    screen.blit(rot_image, rot_image_rect)
    
    play1.collide()
    
    health = int(play1.hp)
    pygame.draw.rect(screen, ((30,30,30)), pygame.Rect(30, 30, 150, 10))
    pygame.draw.rect(screen, ((255,0,0)), pygame.Rect(30, 30, health, 10))
    
    font = pygame.font.SysFont('arial',  50)
    text = font.render(str(int(pl.killed)), True, (255,255,255))
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
    play1.px = 100
    play1.py = 300
    pl.killed = 0
    en.evils.clear()
    en.Bullet_list.clear()
    pl.play_bullets.clear()
    pygame.mixer.music.rewind()

def background():
    for i in range(20):
        pygame.draw.circle(screen, (255,255,255), (randint(0, 1000), randint(0, 700)), 1, 1)


pygame.mixer.music.play(loops=True)

while running: # mimicking game cycle
    
    if play1.hp <= 0:
        lose = pygame.mixer.Sound("wompwomp.wav")
        pygame.mixer.Sound.play(lose)
        youLose = True
        resetGame()
        playing = False
        
    elif pl.killed >= 25:
        youWin = True
        resetGame()
        playing = False
        
    if playing:
        pygame.mixer.music.unpause()
        youWin = False
        youLose = False
        gameDoStuff()
        
    else:
        pygame.mixer.music.pause()
        menuScreen(screen, youWin, youLose)
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()
    
    clock.tick(60)

#meow


