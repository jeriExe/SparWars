import pygame
import Enemy as en
import Player as pl

pygame.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock() # set FPS

running = True

sean = pl.Player()

while running: # mimicking game cycle
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #quit if clicked on X
            
            running = False
            pygame.quit()

    screen.fill((59, 21, 28)) # wipe screen
    
    for enemy in en.evils:
        
        enemy.movement(pl.px, pl.py) # call movement
        enemy.update(screen) #draw new xy
        
        for bullet in en.Bullet_list:
            bullet.Bullet_vector(screen)
    
        
    if pygame.time.get_ticks() % 60 == 0:
         
        for enemy in en.evils:
            b1 = en.Bullet(enemy.rect.centerx, enemy.rect.centery, pl.px, pl.py)
            en.Bullet_list.append(b1)

        if len(en.Bullet_list) > 30:
            en.Bullet_list = en.Bullet_list[(len(en.Bullet_list)//2) :]
    
    keys = pygame.key.get_pressed()
    rot_image, rot_image_rect, angle = sean.rotate()

    pl.px, pl.py = sean.move(pl.px, pl.py, keys)
    for pbullet in pl.play_bullets:
        pbullet.bullet_move()
        pbullet.draw(screen)
    sean.draw_cursor(screen)
    screen.blit(rot_image, rot_image_rect)
    
    pygame.display.flip()
    
    clock.tick(60)