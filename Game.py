import pygame
import Enemy as en
import Player as pl
from random import randint
pygame.init() #init the pygame module 

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height)) #set resolution 

clock = pygame.time.Clock() # set FPS

running = True #bool for while loop

play1 = pl.Player() #create instance of player 

playing = False #playing bool that triggers game starting initialized to false
                
youWin = False 
                #you win/ lose also set to False by default as they trigger end screens
youLose = False 

pygame.mixer.music.load("Act_DS_Escape.wav") #loads the main game soundtrack

def gameDoStuff(): #function that contains main game sequence/updates
    screen.fill((0, 0, 0)) # wipe screens
    
    background() #generates the starfield
    
    if len(en.evils) < 5: #limits number of enemies on screen at once
        if pygame.time.get_ticks() % 100 == 0:    #rate at which enemies can spawn
            respawn = en.Enemy(randint(50, 500), randint(50, 650), randint(3,5)) #generates random position and spawns enemy there
            en.evils.append(respawn) #appends to list so Enemy methods may be applied 
            spawn2 = en.Enemy(randint(550, 950), randint(50, 650), randint(3,5)) #spawns enemy in a different random range
            en.evils.append(spawn2) #appends to list so Enemy methods may be applied 
            
    
    for enemy in en.evils: #updates for each enemy on screen
        enemy.movement(play1.px, play1.py) # call movement
        enemy.update(screen, play1) #draw new xy
        
    for bullet in en.Bullet_list: #updates each bullet position independently
        bullet.Bullet_vector(screen) #Enemy bullet movement 
        
    if pygame.time.get_ticks() %60 == 0:  #rate at which enemy bullets automatically fire
         
        for enemy in en.evils:  #adds a bullet at the enemy position and adds it to list of total bullets
            b1 = en.Bullet(enemy.rect.centerx, enemy.rect.centery, play1.px, play1.py) #creates a new instance of bullet on enemy that moves towards player
            en.Bullet_list.append(b1)  #adds to bullet list such that the enemy bullet methods may be applied 
    
    
    keys = pygame.key.get_pressed() #continuous check, determines which keys are being pressed at any time. gets passed to player
    
    rot_image, rot_image_rect = play1.rotate() #sets player rotation, both the image and the rectangle object 

    play1.px, play1.py = play1.move(keys) #Sean plz explain  player stuff
    
    for pbullet in pl.play_bullets: #will run for each bullet shot by the player
        pbullet.bullet_move() #calls the movement update function from Player module
        pbullet.draw(screen) #blits the bullet & rect on screen
    play1.draw_cursor(screen)  #draws the cursor on screen
    screen.blit(rot_image, rot_image_rect) #places the updated player ship & rotation
    
    play1.collide() #calls collision detection for player
    
    health = int(play1.hp) #compoonents for visual player health bar in corner
    pygame.draw.rect(screen, ((30,30,30)), pygame.Rect(30, 30, 150, 10)) #draws a backdrop
    pygame.draw.rect(screen, ((255,0,0)), pygame.Rect(30, 30, health, 10)) #player health bar, is syncronized with current player health
    
    font = pygame.font.SysFont('arial',  50) #loads font for kill counter
    text = font.render(str(int(pl.killed)), True, (255,255,255)) #will print the updated number of enemies killed
    
    textrect = text.get_rect() #defines a location for the counter and prints it on screen
    textrect.center = (925, 5) #^
    screen.blit(text, textrect.center)#^
    
    pygame.display.flip() # "draws" the changed values and positions 


def menuScreen(screen, youWin, youLose): #displayed whenever "playing" is False; when you start the game and upon losing or winning
    
    #picks certain colour, font and message to display based on win/lose or first attempt. 
    #also scales font to compensate for message length
    if youLose: 
        font_size = 75
        msg = "YOU LOST, PLAY AGAIN?"
        fontColour = (255,12,32)
    elif youWin:
        font_size = 75
        msg = "YIPPIE! PLAY AGAIN?" 
        fontColour = (12,123,32)
    else:
        font_size = 100
        msg = "START"
        fontColour = (155,135,12)
    
    
    fontColour2 = (255, 232, 31) #hover font colour for button 
    screen.fill((0,0,0)) #resets the background to black
    font = pygame.font.SysFont('timesnewroman', font_size) #loads a font to use for message based on font size
    text = font.render(msg, True, (fontColour)) #assigns message and colour based on lose/win/start with anti-aliasing
    textrect = text.get_rect() #gets a rectangle object from the dimensions of the text
    textrect.center = (screen_width//2 - textrect.centerx, 475 -textrect.centery) #assigns value to text
    
    intructions() #shows the unchanging instructions and title screen

        #below checks if the cursor is intersecting the start button
    if textrect.collidepoint(pygame.mouse.get_pos()[0]-(text.get_width()//2), pygame.mouse.get_pos()[1]-(text.get_height()//2)): 
        text = font.render(msg, True, (fontColour2)) #if it's intersecting it makes the text brighter upon hovering
        
        if pygame.mouse.get_pressed()[2]: #now if the mouse is hovering and there is a click start the game
            global playing
            playing = True
    
    screen.blit(text, textrect.center) #blit the text on screen with necessary values colour 
    
    pygame.display.flip() # "draws" the changed values and positions                                                                          


def resetGame(): #resets the game variables such that upon playing a new round it starts "fresh"
    play1.hp = 150 
    play1.px = 100 #resets player positions and hp to the default 
    play1.py = 300
    pl.killed = 0 #resets the kill counter 
    en.evils.clear() #removes all instances of enemy 
    en.Bullet_list.clear() #removes all instances of enemy's bullets
    pl.play_bullets.clear() #removes all instances of Player bullets
    pygame.mixer.music.rewind() # starts the music from the beginning 

def background(): #this draws 20 stars each tick in random places within the screen to create a flickering background 
    for i in range(20):
        pygame.draw.circle(screen, (255,255,255), (randint(0, 1000), randint(0, 700)), 1, 1) #small 1 pixel "circles" - basically just pixels

def intructions(): #main menu messages
    
    instructfont = pygame.font.SysFont('timesnewroman', 50) #font + size for main text
    
    #displays the movement instructions on screen
    instruct = instructfont.render("USE WASD TO MOVE", True, (255,232,31))
    instructrect = instruct.get_rect()
    instructrect.center = (screen_width//2 - instructrect.centerx, 550 -instructrect.centery)
    
    #displays title image on screen
    title = pygame.image.load("Sparwars.png")
    titlerect = title.get_rect()
    titlerect.center = (screen_width//2 - titlerect.centerx, 225 -titlerect.centery)
    screen.blit(title, (titlerect.center))
    
    #displays start intstructions
    instruct2 = instructfont.render("RIGHT CLICK BUTTON TO START", True, (255,232,31))
    instruct2rect = instruct2.get_rect()
    instruct2rect.center = (screen_width//2 - instruct2rect.centerx, 600 -instruct2rect.centery)
    
    #prints the above on screen
    screen.blit(instruct2, instruct2rect.center)
    screen.blit(instruct, instructrect.center)
    

pygame.mixer.music.play(loops=True) #plays the music by default 

while running: # mimicking game cycle
    
    if play1.hp <= 0: #is the player dead?
        
        lose = pygame.mixer.Sound("wompwomp.wav") #sound effect if player loses
        pygame.mixer.Sound.play(lose) 
        
        youLose = True #if your hp drops below 0 you lose and this will ensure the right endscreen is displayed
        playing = False #stop the playing game cycle/loop
        
        resetGame() #reset the game such that upon replaying none of the values save
        
    elif pl.killed >= 25: #have you destroyed 25 enemies?
        
        youWin = True #if you destroy 25 enemies you win! and this will ensure the right endscreen is displayed
        playing = False #stop the playing game cycle/loop
        
        resetGame() #reset the game such that upon replaying none of the values save
        
    if playing:
        
        pygame.mixer.music.unpause() #unpauses the music while playing 
        
        youWin = False #after starting resets win/lose bools to for the subsequent round
        youLose = False
        
        gameDoStuff() #if you're playing the game run the game loop 
        
    else:
        
        pygame.mixer.music.pause() #pauses the game music while on the menu screen
        
        menuScreen(screen, youWin, youLose) #calls the menu screen and displays the relative information based on win/loss booleans
    
    
    for event in pygame.event.get(): #checks for built in pygame events
        
        if event.type == pygame.QUIT: #quit if clicked on X in top right corner
            
            running = False #ends the game loop 
            pygame.quit() #closes the pygame window
    
    clock.tick(60) #sets the tick rate "essentially the frame rate" to 60

#meow


