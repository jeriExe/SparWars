import pygame
import Player  
from random import *

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) #set up screen bounds

x = randint(50, 750) #
y = randint(50, 550) #randomly spawn instances of Enemy 

class Enemy():
    def __init__(self, x, y):

        self.hp = 100
        self.original_image = self.image = pygame.image.load("ship_little.png")
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.veloY = 1
        self.veloX = 1
        self.screen_width, self.screen_height = screen_width, screen_height

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self):
        mouse_position = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouse_position[0] - self.rect.centerx, mouse_position[1] - self.rect.centery)
        self.rotate(direction.angle_to(pygame.math.Vector2(1, 0)))

        self.rect.x += self.veloX
        self.rect.y += self.veloY

        if not 0 <= self.rect.x <= self.screen_width - self.rect.width:
            self.veloX = -self.veloX
        if not 0 <= self.rect.y <= self.screen_height - self.rect.height:
            self.veloY = -self.veloY

    def draw(self, screen):
        
            
        screen.blit(self.image, self.rect.topleft)

class Bullet():
    def __init__(self, x, y):
        self.bx = x
        self.by = y
        self.image = pygame.draw.circle(screen, (255, 0, 0), (self.bx, self.by), 5)
        
    def Bullet_vector(self):
        diff_x = (Player.x - self.bx)
        diff_y = (Player.y - self.by)
        
        self.bx += (diff_x/10)
        self.by += (diff_y/10)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.bx), int(self.by)), 5)
        
player = Player.Player()

evils = [Enemy(x, y),
         Enemy(randint(50, 750), randint(50, 550)),
         Enemy(randint(50, 750), randint(50, 550))]

Bullet_list = []



clock = pygame.time.Clock() # set FPS

running = True

while running: # mimicking game cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit if clicked on X
            running = False
            pygame.quit()

    screen.fill((0, 0, 0)) # wipe screen
    
    if pygame.time.get_ticks() % 60 == 0:
            b1 = Bullet(x, y)
            Bullet_list.append(b1)
    
    
    
    for bullet in Bullet_list:
        bullet.Bullet_vector()
    
    for enemy in evils:
        enemy.movement() # call movement
        enemy.draw(screen) #draw new xy

    pygame.display.flip()
    clock.tick(60)
