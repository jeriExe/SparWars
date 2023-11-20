import pygame
import math  
from random import randint

class Enemy():
    def __init__(self, x, y, randvelo):
        self.x = x
        self.y = y
        self.hp = 100
        self.original_image = self.image = pygame.image.load("CABT13.png")
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.veloY = self.veloX = randvelo
         
        

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self, playX, playY):
        direction = pygame.math.Vector2(playX - self.rect.x, playY - self.rect.y)
        self.rotate(direction.angle_to(pygame.math.Vector2(1, 0)))

        self.rect.x += self.veloX
        self.rect.y += self.veloY

        if self.rect.left < 0:
            self.rect.left = 10
            self.veloX = -self.veloX

        if self.rect.right > 1000:
            self.rect.right = 990
            self.veloX = -self.veloX

        if self.rect.top < 0:
            self.rect.top = 10
            self.veloY = -self.veloY

        if self.rect.bottom > 700:
            self.rect.bottom = 695
            self.veloY = -self.veloY
        

    def update(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in Bullet_list:
            if self.rect.colliderect(bullet.rect) and bullet.ttc < 0:
                self.hp -= 10
                Bullet_list.remove(bullet)
        if self.hp < 10:
                evils.remove(self)   
        


class Bullet():
    def __init__(self, spawnX, spawnY, playX, playY):
        
        self.ttc = 40
        self.bx = spawnX
        self.by = spawnY
        
        self.radius = 5
        
        
        self.rect = pygame.Rect(self.bx - self.radius, self.by - self.radius, 2 * self.radius, 2 * self.radius)
        
        self.theta = math.atan2(playY - self.by, playX - self.bx)

    def Bullet_vector(self, screen):
        
        v = 5
        
        self.bx += v * math.cos(self.theta)
        self.by += v * math.sin(self.theta)
        
        self.ttc -= 1
        
        pygame.draw.circle(screen, (255, 0, 0), (int(self.bx), int(self.by)), self.radius)
        
        
evils = [Enemy(randint(50, 550), randint(50, 550), randint(2,4)), 
         Enemy(randint(50, 550), randint(50, 550), randint(4,6)),
         Enemy(randint(50, 550), randint(50, 550), randint(4,6))]

Bullet_list = []

