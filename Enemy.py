import pygame
import math  
from random import randint

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.original_image = self.image = pygame.image.load("CABT13.png")
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.veloY = 5
        self.veloX = 5
        

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
        

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Bullet():
    def __init__(self, screen, spawnX, spawnY, playX, playY):
        
        self.bx = spawnX
        self.by = spawnY
        
        self.theta = math.atan2(playY - self.by, playX - self.bx)

    def Bullet_vector(self, screen):
        
        v = 3
        
        self.bx += v * math.cos(self.theta)
        self.by += v * math.sin(self.theta)
        
        
        
        pygame.draw.circle(screen, (255, 0, 0), (int(self.bx), int(self.by)), 5)
        
        
evils = [Enemy(randint(50, 550), randint(50, 550)),
         Enemy(randint(50, 550), randint(50, 550)),
         Enemy(randint(50, 550), randint(50, 550))]

Bullet_list = []

