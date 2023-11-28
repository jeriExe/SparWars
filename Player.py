import pygame
import math

px = 100
py = 300
play_bullets = []

class Player:
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.dmg = 30

    def move(self, px, py, keys):
        fire = False
        ship = pygame.image.load("ship_little.png").convert_alpha()
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        move_down = keys[pygame.K_s]
        move_up = keys[pygame.K_w]

        if move_left:
            px -= 5.5
        if move_right:
            px += 5.5
        if move_down:
            py += 5.5
        if move_up:
            py -= 5.5

        left, middle, right = pygame.mouse.get_pressed()
        if left:
            if pygame.time.get_ticks() %5 == 1:
                play_bullets.append(PlayBullet(px, py))
                #fire = True 
  
        #if fire:
            #play_bullets.append(PlayBullet(px, py))

        if px >= 1000 - 0.5 * ship.get_width():
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
        ship_rect = ship.get_rect(center=player_pos)

        mouse_px, mouse_y = pygame.mouse.get_pos()
        rel_px, rel_py = mouse_px - px, mouse_y - py
        angle = (180 / math.pi) * -math.atan2(rel_py, rel_px)
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center=ship_rect.center)

        return rot_image, rot_image_rect.topleft, angle

class PlayBullet:
    def __init__(self, bx, by):
        
        self.ttc = 20
        self.radius = 5
        self.m_x, self.m_y = pygame.mouse.get_pos()
        
        self.rect = pygame.Rect(bx +1, by+1, 2, 2)
        
        self.theta = math.atan2(self.m_y - by, self.m_x - bx)
        
    def bullet_move(self):
        speed = 10
        
        self.rect.centerx += int(speed * math.cos(self.theta))
        self.rect.centery += int(speed * math.sin(self.theta))
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), ((self.rect.centerx), (self.rect.centery)), self.radius)
            
