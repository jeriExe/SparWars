import pygame
from random import *

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) #set up screen bounds

x = randint(1, 799) #
y = randint(1, 599) #randomly spawn instances of Enemy 

class Enemy():
    def __init__(self, x, y):
        super().__init__()

        self.hp, self.dmg = 100, 10
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



evil = Enemy(x, y)



clock = pygame.time.Clock() # set FPS

running = True

while running: # mimicking game cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit if clicked on X
            running = False
            pygame.quit()

    screen.fill((0, 0, 0)) # wipe screen

    evil.movement() # call movement
    evil.draw(screen) #draw new xy

    pygame.display.flip()
    clock.tick(60)
