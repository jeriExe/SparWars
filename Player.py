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
        self.hp = 100 #starting hit points

    def move(self, px, py, keys): #function to handle movement of player + creation of bullets
        ship = pygame.image.load("ship_little.png").convert_alpha() #loads the png for the player ship
        
        move_left = keys[pygame.K_a] #defines the keys "w,a,s,d" as movement controls, detecting if any are pressed down
        move_right = keys[pygame.K_d] #keys evaluates to a boolean, will return true if pressed down
        move_down = keys[pygame.K_s]
        move_up = keys[pygame.K_w]

        if move_left: #will adjust the player position (x or y value) depending on key pressed
            px -= 5.5
        if move_right:
            px += 5.5
        if move_down:
            py += 5.5
        if move_up:
            py -= 5.5

        left, middle, right = pygame.mouse.get_pressed() #detects if mouse/touchpad keys are clicked (boolean)
        if left:
            if pygame.time.get_ticks() %5 == 1: #sets a reduced rate of fire -> will create a bullet at a continuous delayed rate
                play_bullets.append(PlayBullet(px, py)) #adds a bullet to the bullet list, with the x/y coordiantes where it was fired
                

        if px >= 1000 - 0.5 * ship.get_width():  #checks to keep player within the screen, by adjusting x/y values if going off screen
            px = 1000 - 0.5 * ship.get_width()
        if px <= 0 + 0.5 * ship.get_width():
            px = 0 + 0.5 * ship.get_width()
        if py >= 700 - 0.5 * ship.get_height():
            py = 700 - 0.5 * ship.get_height()
        if py <= 0 + 0.5 * ship.get_height():
            py = 0 + 0.5 * ship.get_height()
            
        return px, py

    def draw_cursor(self, screen):
        aim_px, aim_py = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (0, 255, 0), (aim_px, aim_py), 15, 3)

    def rotate(self):
        ship = pygame.image.load("ship_little.png").convert_alpha()

        player_pos = [px, py]
        self.ship_rect = ship.get_rect(center=player_pos)

        mouse_px, mouse_y = pygame.mouse.get_pos()
        rel_px, rel_py = mouse_px - px, mouse_y - py
        angle = (180 / math.pi) * -math.atan2(rel_py, rel_px)
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center=self.ship_rect.center)

        return rot_image, rot_image_rect.topleft, angle
    
    def collide(self):
        for bullet in en.Bullet_list:
            if self.ship_rect.colliderect(bullet.rect): #if there is a collision and it has been the neccessary number of ticks
                self.hp -= 10 #remove 10 hp
                en.Bullet_list.remove(bullet) #remove the bullet
            #if self.hp < 0:
                #pygame.quit()
                
class PlayBullet:
    def __init__(self, bx, by):
        
        self.ttc = 20
        self.radius = 5
        self.m_x, self.m_y = pygame.mouse.get_pos()
        
        self.rect = pygame.Rect(bx +1, by+1, 2, 2)
        
        self.theta = math.atan2(self.m_y - by, self.m_x - bx)
        
    def bullet_move(self):
        speed = 13
        
        self.rect.centerx += int(speed * math.cos(self.theta))
        self.rect.centery += int(speed * math.sin(self.theta))
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), ((self.rect.centerx), (self.rect.centery)), self.radius)
            
