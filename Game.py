import pygame
import Enemy as en
import Player as pl

pygame.init() #init the pygame mod

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height)) #set resolution 

clock = pygame.time.Clock() # set FPS

running = True #bool for while loop

play1 = pl.Player()



def gameDoStuff():
    screen.fill((59, 21, 28)) # wipe screen
    
    for enemy in en.evils:
        
        enemy.movement(pl.px, pl.py) # call movement
        enemy.update(screen) #draw new xy
        
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
    
    pygame.display.flip()

playing = False

def menuScreen(screen):
    if pygame.mouse.get_pos()[0] > 50 and pygame.mouse.get_pos()[1] >50:
        print("True")
        fontColour = (0,0,0)
    else:
        fontColour =(255,255,255)
    screen.fill((34,34,34))
    font = pygame.font.SysFont('timesnewroman',  200)
    text = font.render('Start', True, (fontColour))
    textrect = text.get_rect()
    textrect.center = (screen_width//2 - textrect.centerx, screen_height//2 -textrect.centery)
    screen.blit(text, textrect.center)
    
    
    pygame.display.flip()

while running: # mimicking game cycle
    if playing:
        gameDoStuff()
    else:
        menuScreen(screen)
            
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()

    
    
    
    
    clock.tick(60)
    