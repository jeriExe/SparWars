import pygame
import Player
import math  
from random import *


pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) #set up screen bounds



class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.original_image = self.image = pygame.image.load("ship_little.png")
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.veloY = 1
        self.veloX = 1
        

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self):
        direction = pygame.math.Vector2(Player.px - self.rect.x, Player.px - self.rect.y)
        self.rotate(direction.angle_to(pygame.math.Vector2(1, 0)))

        self.rect.x += self.veloX
        self.rect.y += self.veloY

        if not 0 <= self.rect.x <= screen_width - self.rect.width:
            self.veloX = -self.veloX
        if not 0 <= self.rect.y <= screen_height - self.rect.height:
            self.veloY = -self.veloY
        return self.rect.x, self.rect.y

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bullet():
    def __init__(self, spawnX, spawnY, playX, playY):
        self.bx = spawnX
        self.by = spawnY
        self.image = pygame.draw.circle(screen, (255, 0, 0), (self.bx, self.by), 5)
        self.theta = math.atan((playY - self.by)/(playX - self.bx)+0.1)
        
    def Bullet_vector(self):
        
        
        v = -3
        
        self.bx += v*math.sin(self.theta)
        self.by += v*math.cos(self.theta)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.bx), int(self.by)), 5)
        return self.bx, self.by
        
play1 = Player.Player()

evils = [Enemy(randint(50, 550), randint(50, 550)),
         Enemy(randint(50, 550), randint(50, 550)),
         Enemy(randint(50, 550), randint(50, 550))]

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
    
    for enemy in evils:
        for bullet in Bullet_list:
            bullet.Bullet_vector()
            
    if pygame.time.get_ticks() % 60 == 0:
        for enemy in evils:
            b1 = Bullet(enemy.rect.centerx, enemy.rect.centery, 300, 300)
            Bullet_list.append(b1)
    
    
    

    pygame.display.flip()
    clock.tick(60)
