import pygame
from random import *
import math
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) #set up screen bounds

x = randint(1, 799) #
y = randint(1, 599) #randomly spawn instances of Enemy 

p = randint(1, 799) #
w = randint(1, 599)

class Enemy():
    def __init__(self, p, w):
        super().__init__()

        self.hp, self.dmg = 100, 10
        self.original_image = self.image = pygame.image.load("ship_little.png")
        self.rect = self.image.get_rect(topleft=(p, w))  
        self.veloY = 1
        self.veloX = 4
        self.screen_width, self.screen_height = screen_width, screen_height

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self):
        mouse_position = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(x - self.rect.centerx, y - self.rect.centery)
        self.rotate(direction.angle_to(pygame.math.Vector2(1, 0)))

        self.rect.x += self.veloX
        self.rect.y += self.veloY

        if not 0 <= self.rect.x <= self.screen_width - self.rect.width:
            self.veloX = -self.veloX
        if not 0 <= self.rect.y <= self.screen_height - self.rect.height:
            self.veloY = -self.veloY

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


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
            x -= 3
        if move_right:
            x += 3
        if move_down:
            y += 3
        if move_up:
            y -= 3
            
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
    
        return rot_image, rot_image_rect.topleft
    
class PlayBullet:
    def __init__(self):
        pass
    def bullet_move(self, x, y):
        pass


Play1 = Player()



evil = Enemy(x, y)



clock = pygame.time.Clock() # set FPS

running = True

while running: # mimicking game cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit if clicked on X
            running = False
            pygame.quit()

    screen.fill((0, 0, 0)) # wipe screen

    evil.movement() # call movement
    evil.draw(screen) #draw new xy
    
    ship = pygame.image.load("ship_little.png").convert_alpha()
    keys = pygame.key.get_pressed()
    rot_image, rot_image_rect = Play1.rotate()
    
    x, y = Play1.move(x, y, keys)
    Play1.draw_cursor()
    screen.blit(rot_image, rot_image_rect)
    bullet = pygame.image.load("pbullet.png").convert_alpha()

    pygame.display.flip()
    clock.tick(60)
