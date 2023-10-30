import pygame
import math
pygame.init()

x = 100
y = 300

class Player:
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.dmg = 30

    def move(self, x, y, keys):
        ship = pygame.image.load("ship_little.png").convert_alpha()
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        move_down = keys[pygame.K_s]
        move_up = keys[pygame.K_w]

        if move_left:
            x -= 1.5
        if move_right:
            x += 1.5
        if move_down:
            y += 1.5
        if move_up:
            y -= 1.5
            
        if x >= 1000-0.5*ship.get_width():
            x = 1000-0.5*ship.get_width()
        if x <= 0 + .5*ship.get_width():
            x = 0 + .5*ship.get_width()
        if y >= 700-0.5*ship.get_height():
            y = 700-0.5*ship.get_height()
        if y <= 0 + 0.5*ship.get_height():
            y = 0 + 0.5*ship.get_height()
        return x, y

    def draw_cursor(self):
        aim_x, aim_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (0, 255, 0), (aim_x, aim_y), 15, 3)
    
    def rotate(self):
        
        ship = pygame.image.load("ship_little.png").convert_alpha()
        
        player_pos  = [x, y]
        ship_rect = ship.get_rect(center = player_pos)
    

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center = ship_rect.center)
    
        return rot_image, rot_image_rect.topleft, angle
    
class PlayBullet:
    def __init__(self):
        pass

    def bullet_rotate(self):
        bullet = pygame.image.load("pbullet_small.png").convert_alpha()
        player_pos  = [x, y]
        bull_rect = bullet.get_rect(center = player_pos)
        
        rot_bull = pygame.transform.rotate(bullet, angle)
        rot_bull_rect = rot_bull.get_rect(center = bull_rect.center)
        spawn = keys[pygame.K_r]
        if spawn:
            show = (screen.blit(rot_bull, rot_bull_rect.topleft))
            return show
    def bullet_move(self):
        pass
            
Play1 = Player()
screen = pygame.display.set_mode((1000, 700))
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
      
    keys = pygame.key.get_pressed()    
    rot_image, rot_image_rect, angle = Play1.rotate()
        
    PlayBullet.bullet_rotate(keys)
    x, y = Play1.move(x, y, keys)
    Play1.draw_cursor()
    PlayBullet.bullet_rotate(keys)
    screen.blit(rot_image, rot_image_rect)
      
    
    pygame.display.flip()

pygame.quit()
