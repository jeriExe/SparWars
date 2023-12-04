import pygame #pygame module for game logic
import math #math for vector and angle calculations 
import Player as pl # Player accessed to iterate through it's bullet list and up the kill counter 


class Enemy(): #class with enemy specfic inherited functions 
    
    def __init__(self, x, y, randvelo): #all enemies inherit the following traits
        
        self.x = x 
        self.y = y  
                        #sets initial x,y posisition and hp
        self.hp = 80 
        
        self.original_image = self.image = pygame.image.load("tie_fighter.png") #sets the image based on a relative path
        self.rect = self.image.get_rect(topleft=(x, y)) #sets rectangle object based on image dimensions 
        
        self.veloY = self.veloX = randvelo #gives the x,y velocities a random value (4-6px)

    def movement(self, playX, playY): #logic for enemy movement
        
        direction = pygame.math.Vector2(playX - self.rect.x, playY - self.rect.y) #uses pygame vector to get aim direction; this makes the enemy aim at player
        self.image = pygame.transform.rotate(self.original_image, direction.angle_to(pygame.math.Vector2(0,0))) #uses pygame image rotation with respect to origin
        self.rect = self.image.get_rect(center=self.rect.center) #sets the rect object to the image rotation about the center 
        
        self.rect.x += self.veloX #displaces by x velocity 
        self.rect.y += self.veloY #displaces by y velocity 

        #following checks if enemy is out of bounds and if it is sets the location to 10 pixels in from the bounds and reverses direction
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
            self.rect.bottom = 690
            self.veloY = -self.veloY
        
    def update(self, screen, play1): #updates anything important for enemy
                
        
        screen.blit(self.image, self.rect.topleft) #this sets the new image location based on the recalculated rectangle
        
        
        for bullet in pl.play_bullets: #iterates through each instance of bullet in player's list of bullets
            
            if self.rect.colliderect(bullet.rect): #if the enemy is colliding with one of the instances 
                
                self.hp -=10 #reduce the enemy's hp by 10
                
                pl.play_bullets.remove(bullet) #remove the instance of bullet from the player's bullet list as to not have any more collisions
             
        if self.hp <= 0: #checks for enemy's death i.e. health below / == 0
            
            screen.blit(pygame.image.load("splosion.png"), (self.rect.x, self.rect.y)) #blit an explosion on enemy's place of death 
            pygame.time.wait(20) #wait 20ms for explosion to successfully display  
            
            evils.remove(self) #remove instance of enemy who's hp is below 0
            pl.killed += 1 # add one to player's "score"
            
            if play1.hp >= 100: #siphon for the player, gains back 50 health for every kill to a maximum of 150hp
                play1.hp = 150
            else:
                play1.hp += 50
                           
        
class Bullet(): #class with bullet specfic inherited functions 
    
    def __init__(self, spawnX, spawnY, playX, playY): #bullet inherits from the following qualities 
        
        self.radius = 5 #bullet circle radius 
        
        self.rect = pygame.Rect(spawnX +1, spawnY+1, 2, 2) #rectangle for collisions 
        
        self.theta = math.atan2(playY - spawnY, playX - spawnX) #given an angle to compute movement, 
                                    #the angle is with respect to the enemy to shoot towards player

        self.v = 15  #bullet velocity 

    def Bullet_vector(self, screen): #vector and angle math for enemy's bullets
        
        self.rect.centerx += int(self.v * math.cos(self.theta)) #increases or decreases x value based on players location relative to enemy
        self.rect.centery += int(self.v * math.sin(self.theta)) #increases or decreases y value based on players location relative to enemy
        
        pygame.draw.circle(screen, (0, 255, 0), ((self.rect.centerx), (self.rect.centery)), self.radius)# redraw the circle after the calculation
        
        if self.rect.centerx > 1000 or self.rect.centerx < 0 or self.rect.centery > 700 or self.rect.centerx < 0: 
                            #when the bullet "leaves" the screen remove it as to not waste resources on meaningless calcs
            Bullet_list.remove(self) 
        
        
evils = [] #list of enemies set to be empty upon starting the game, populated in game loop

Bullet_list = [] #bullet list to iterate and append when enemy shoots

