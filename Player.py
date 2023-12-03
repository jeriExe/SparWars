import pygame
import Enemy as en
import math

#defining starting place for player ship
px = 100
py = 300


play_bullets = [] #creating empty list to store bullets when fired
killed = 0 #setting the value of enemies eliminated to zero

class Player:
    def __init__(self): #the basic values associated to the player
        
        self.hp = 150 #starting hit points
        self.ship = pygame.image.load("x_wing.png").convert_alpha() #loads the png for the player ship
        
    def move(self, px, py, keys): #function to handle movement of player + creation of bullets
        
        move_left = keys[pygame.K_a] #defines the keys "w,a,s,d" as movement controls, detecting if any are pressed down
        move_right = keys[pygame.K_d] #keys evaluates to a boolean, will return true if pressed down
        move_down = keys[pygame.K_s]
        move_up = keys[pygame.K_w]

        if move_left: #will adjust the player position (x or y value) depending on key pressed
            px -= 8
        if move_right:
            px += 8
        if move_down:
            py += 8
        if move_up:
            py -= 8

        left = pygame.mouse.get_pressed()[0] #detects if mouse/touchpad keys are clicked (boolean)
        if left:
            if pygame.time.get_ticks() %5 == 1: #sets a reduced rate of fire -> will create a bullet at a continuous delayed rate
                play_bullets.append(PlayBullet(px, py)) #adds a bullet to the bullet list, with the x/y coordiantes where it was fired
                

        if px >= 1000 - 0.5 * self.ship.get_width():  #checks to keep player within the screen, by adjusting x/y values if going off screen
            px = 1000 - 0.5 * self.ship.get_width()
        if px <= 0 + 0.5 * self.ship.get_width():
            px = 0 + 0.5 * self.ship.get_width()
        if py >= 700 - 0.5 * self.ship.get_height():
            py = 700 - 0.5 * self.ship.get_height()
        if py <= 0 + 0.5 * self.ship.get_height():
            py = 0 + 0.5 * self.ship.get_height()
            
        return px, py  #returns the updated player position 

    def draw_cursor(self, screen): 
        aim_px, aim_py = pygame.mouse.get_pos() #grabs cooridnates for cursor from mouse position
        pygame.draw.circle(screen, (0, 255, 0), (aim_px, aim_py), 15, 3) #draws a cursor at the mouse position

    def rotate(self): 
        player_pos = [px, py] #creates a list containing the player's current position
        self.ship_rect = (self.ship).get_rect(center=player_pos) #creates a rect on top of the player

        mouse_px, mouse_y = pygame.mouse.get_pos() #gets and stores the current cursor position
        rel_px, rel_py = mouse_px - px, mouse_y - py #calculates the distance between player and cursor in both x and y
        angle = (180 / math.pi) * -math.atan2(rel_py, rel_px) #calculates the angle from the player to the cursor
        rot_image = pygame.transform.rotate(self.ship, angle) #rotates the ship png according to the angle
        rot_image_rect = rot_image.get_rect(center=self.ship_rect.center) #rotates the rect of the player

        return rot_image, rot_image_rect.topleft #returns the rotated image, the rotated rect, and the calculated angle
    
    def collide(self):
        for bullet in en.Bullet_list: #will run for every bullet created
            if self.ship_rect.colliderect(bullet.rect): #if there is a collision and it has been the neccessary number of ticks
                self.hp -= 10 #remove 10 hp
                en.Bullet_list.remove(bullet) #remove the bullet
            

        
class PlayBullet:
    def __init__(self, bx, by):
        
        self.ttc = 20 #timer to avoid collision with own bullet
        self.radius = 5 #radius of bullet
        self.m_x, self.m_y = pygame.mouse.get_pos() #stores current mouse position
        
        self.rect = pygame.Rect(bx +1, by+1, 2, 2) #creates a rect on top of each bullet
        
        self.theta = math.atan2(self.m_y - by, self.m_x - bx) #calculates angle of travel for the bullet from player to cursor
        
    def bullet_move(self):
        speed = 15 #how fast the bullet will move
        
        self.rect.centerx += int(speed * math.cos(self.theta)) #adjusts the bullet rect according to speed and angle
        self.rect.centery += int(speed * math.sin(self.theta))
        
        if self.rect.centerx > 1000 or self.rect.centerx < 0 or self.rect.centery > 700 or self.rect.centerx < 0:
            play_bullets.remove(self) #checks if out of bounds, deletes bullet if it is
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), ((self.rect.centerx), (self.rect.centery)), self.radius)
         #draws the bullet w/ its rect on top