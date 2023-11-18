import pygame
import math

pygame.init()

px = 100
py = 300
play_bullets = []
trick = []
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
            px -= 1.5
        if move_right:
            px += 1.5
        if move_down:
            py += 1.5
        if move_up:
            py -= 1.5

        left, middle, right = pygame.mouse.get_pressed()
        left = True
        if left:
            #fire = True 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        fire = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        fire = False
                        
        if fire:
            play_bullets.append(PlayBullet(px, py))

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
        self.bx = bx
        self.by = by
        self.radius = 5
        self.m_x, self.m_y = pygame.mouse.get_pos()
        self.flame = pygame.image.load("kisspng-pixel-art-nyan-cat-5b36ad7a374e81.0343808815303100102266.png")
    def bullet_move(self):
        diff_px = (self.m_x - self.bx)
        diff_py = (self.m_y - self.by)
        self.distance = (math.sqrt(diff_px ** 2 + diff_py ** 2))
    
        if self.distance>10:
            speed = 10
            direction_x = diff_px/self.distance
            direction_y = diff_py/self.distance
            self.bx += speed * direction_x
            self.by += speed * direction_y
        if self.distance < 15:
            screen.blit(self.flame, (self.bx, self.by))
            #check for collision    
            
    def draw(self, screen):
        if self.distance > 5:
            pygame.draw.circle(screen, (255, 0, 255), (int(self.bx), int(self.by)), self.radius)

play1 = Player()
screen = pygame.display.set_mode((1000, 700))

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    rot_image, rot_image_rect, angle = play1.rotate()

    px, py = play1.move(px, py, keys)
    for pbullet in play_bullets:
        pbullet.bullet_move()
        pbullet.draw(screen)
    play1.draw_cursor(screen)
    screen.blit(rot_image, rot_image_rect)

    

    pygame.display.flip()

pygame.quit()
