import pygame
import math  
import Player as pl


class Enemy():
    def __init__(self, x, y, randvelo): #all enemies inherit the following traits
        self.x = x 
        self.y = y
        self.hp = 80 #sets x,y hp
        self.original_image = self.image = pygame.image.load("tie_fighter.png") #sets the image
        self.rect = self.image.get_rect(topleft=(x, y)) #sets rect object 
        self.veloY = self.veloX = randvelo #gives the x,y velocities a random value 

    def movement(self, playX, playY): 
        direction = pygame.math.Vector2(playX - self.rect.x, playY - self.rect.y) #uses vector to get aim direction
        self.image = pygame.transform.rotate(self.original_image, direction.angle_to(pygame.math.Vector2(0,0))) #uses pygame image rotation with respect to origin
        self.rect = self.image.get_rect(center=self.rect.center) #sets the rect obj to the image rotation about the center 
        
        self.rect.x += self.veloX #displaces by x velo
        self.rect.y += self.veloY #displaces by y velo

        #following checks if enemy is out of bounds and if it is sets the location to 5 pixels in from the bounds and reverses direction
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
        
         

    def update(self, screen, play1): #updates anything important for enemy
                
        
        screen.blit(self.image, self.rect.topleft)
        
        
        for bullet in pl.play_bullets:
            if self.rect.colliderect(bullet.rect): 
                
                self.hp -=1
                pl.play_bullets.remove(bullet)
             
        if self.hp < 0: #if the enemy's hp falls below 0 remove it
            
            screen.blit(pygame.image.load("splosion.png"), (self.rect.x, self.rect.y))
            pygame.time.wait(50)
            
            evils.remove(self)  
            pl.killed += 1
                
            if play1.hp >= 100:
                play1.hp = 150
            else:
                play1.hp += 50
                           
        
class Bullet():
    def __init__(self, spawnX, spawnY, playX, playY): #bullet inherits 
        
        self.ttc = 20 #gets a tick counter to ensure so early collision occur 
        
        self.radius = 5 #bullet circle radius
        
        self.rect = pygame.Rect(spawnX +1, spawnY+1, 2, 2) #rectangle for collisions 
        
        self.theta = math.atan2(playY - spawnY, playX - spawnX) #given an angle to compute movement 

        self.v = 15  #bullet velocity 



    def Bullet_vector(self, screen):
        
        
        
        self.rect.centerx += int(self.v * math.cos(self.theta)) #calc left/right  
        self.rect.centery += int(self.v * math.sin(self.theta)) #calc up/down
        
        pygame.draw.circle(screen, (0, 255, 0), ((self.rect.centerx), (self.rect.centery)), self.radius)#draw the circle 
        
        if self.rect.centerx > 1000 or self.rect.centerx < 0 or self.rect.centery > 700 or self.rect.centerx < 0:
            Bullet_list.remove(self)
        
        
evils = []

Bullet_list = [] #bullet list to iterate and append when shot 

