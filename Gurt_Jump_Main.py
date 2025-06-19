#Coding notes: we should program stuff in linear progression of the game
#This meaning like we program everything for level 1 first, then everything for level 2, and so on
#place the py file in gurt file
#Importing Functions
import pygame
import random
import math
import sys
import tkinter as tk
from tkinter import messagebox
import os


pygame.init()

#Game setup:
WIDTH, HEIGHT = 1024, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"GURT JUMP WOOOOOOO! Level: ")
FONT = pygame.font.SysFont("comisans", 40)

#INSIDE OF THE GAME LOOP

FPS = 30
clock = pygame.time.Clock()
scrn = pygame.display.set_mode((1024, 720))
import pygame


#Various placeholder colours
GREEN = (50, 205, 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
ORANGE = (100, 64, 0)
LIGHT_BLUE = (173, 216, 230)

#Various Global Variables
Player_Width = 200
Player_Height = 200
Player_Speed = 20
Jump_Strength = -20
Gravity = 1



#Classes



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("the gurt.png")
        #self.image.fill("pixil-layer-gurt 30x24.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False

    # Edit this so velocity slowly increases as you hold BUT CAPS OUT AT A MAX VELOCITY
    def update(self, platforms, level):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= Player_Speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += Player_Speed
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = Jump_Strength 
            self.on_ground = False

        # Apply gravity
        self.vel_y += Gravity 
        self.rect.y += self.vel_y 

        # Check for collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if self.vel_y < 0: # Headbutting (slightly buggy)
                    self.vel_y = 0
                    self.rect.top = platform.rect.bottom



    def Player_Respawn(self, level): # Sets the players x/y coords according to what level they are in, also sets velocity to 0
        if level.current_level == 1:
            self.rect.x = 10
            self.rect.y = 10
            self.vel_y = 0
        if level.current_level == 2:
            self.rect.x = 100
            self.rect.y = 600
            self.vel_y = 0
        if level.current_level == 3:
            self.rect.x = 100
            self.rect.y = 600
            self.vel_y = 0

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("pixil-frame-0_3.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_background_image(self, level):
        if level.current_level == 2:
            self.image = pygame.image.load("pixil-frame-0_4.png")



        

class FakeCheckpoint():
    pass



class Portal(pygame.sprite.Sprite): # Also used as master class for some classes
    # Subclasses = Gurterade
    def __init__(self, x, y, width, height):
        super().__init__()
        #self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("checkpoint.png")
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)



class Gurterade(Portal):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        #self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("gurtarade.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Spikes(pygame.sprite.Sprite): # Also master class for fake Checkpoint
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED) #Replace with the actual image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN) #Replace with the actual image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class First_Teleporter(Portal): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        #self.image = pygame.image.load("blue port.png")
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Second_Teleporter(Portal): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        #self.image = pygame.image.load("small port 1.png")
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Jumppad(): 
    pass



class Level:
    def __init__(self):
        #self.current_level = 1
        self.current_level = 1 #For testing only
        self.platforms = []
        self.platform_group = pygame.sprite.Group()
        self.portal = None
        self.lava = None
        self.gurterade = None
        self.spikes = []
        self.first_teleporter = None
        self.second_teleporter = None
        self.background = None
        
        self.load_level()
        self.gerteradeCollected = False
      
        
    def load_level(self): # Loads the level, first by settting variables back to default, then making them again to 'craft' the level
        #59 552
        self.platforms = []
        self.spikes = []
        self.gurterade = None
        self.first_teleporter = None
        self.second_teleporter = None
        self.gerteradeCollected = False
        if self.current_level == 1:
            
            #Platform(X, Y, Width, Height)
            self.platforms = [ #Not finished
                Platform(294, 291, 280, 48),
                Platform(587, 457, 327, 48),
                Platform(59, 552, 327, 48),
                Platform(0, 100, 295, 233),
                #Platform(0, )
            ]
            self.spikes = [
                Spikes(-1000,740, 102400, 10) #This spike is to kill the player when they "fall out of the map."
            ]
            self.portal = Portal(300, 552-75, 75, 75)
            self.gurterade = Gurterade(800, 350, 50, 50)
            self.first_teleporter = First_Teleporter(903, 312, 81, 138)
            self.second_teleporter = Second_Teleporter(9, 349, 100, 135)
            self.background = Background(0,0, 1080, 720)
        if self.current_level == 2:
            #Platform(X, Y, Width, Height)
            self.platforms = [ #Placeholder variables
                Platform(0, HEIGHT - 20, WIDTH, 20),
                Platform(0, 604, 185, 48),
                Platform(26, 265, 300, 48),
                Platform(163, 463, 300, 48),
                Platform(493, 341, 300, 48),
                Platform(876, 620, 300, 48)

            ]
            self.portal = Portal(850, 550, 75, 75)
            self.gurterade = Gurterade(800, 350, 50, 50)
            self.background = Background(0,0, 1080, 720)
        if self.current_level == 3:
            #Platform(X, Y, Width, Height)
            self.platforms = [ #Placeholder variables
                Platform(0, HEIGHT - 20, WIDTH, 20),
                Platform(400, 600, 100, 20),
                Platform(300, 475, 120, 20),


            ]
            self.portal = Portal(850, 550, 75, 75)
            self.spikes = [
                Spikes(650, 650, 75, 75)

            ]
            self.gurterade = Gurterade(800, 350, 50, 50)


            

        self.platform_group = pygame.sprite.Group((self.platforms) +  (self.spikes))
        self.portal_group = pygame.sprite.Group(self.portal)
        if self.gurterade: # Only makes the group if gurterade exists (kinda useless but might do something with it later)
            self.gurterade_group = pygame.sprite.Group(self.gurterade)
        if self.first_teleporter and self.second_teleporter:
            self.teleporter_group = pygame.sprite.Group([self.first_teleporter] + [self.second_teleporter])
        else:
            self.teleporter_group = None
        self.background_group = pygame.sprite.Group(self.background)
 
    def next_level(self, player):
        self.current_level += 1
        player.Player_Respawn(self)

        self.load_level()

    def get_current_level(self):
        return self.current_level




class timer():
    def __init__(self):
        pass

#Game
def main():
    player = Player(10, 10) #This will be over-riden and maybe deleted 
    player_group = pygame.sprite.Group(player)

    level = Level()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player_group.update(level.platforms, level) #Update player

        for spike in level.spikes:
            if player.rect.colliderect(spike.rect): 
                level.load_level()
                player.Player_Respawn(level)


        if level.gurterade.check_collision(player):
            level.gerteradeCollected = True # Update later to work
            level.gurterade.rect.topleft = (965,-10) # Moves the Gurterade

        if level.gerteradeCollected == True: # Checks to see if player collides with goal only when gurterade collected
            if level.portal.check_collision(player):
                level.next_level(player)

        try:
            if level.first_teleporter.check_collision(player):
                player.rect.x = level.second_teleporter.rect.x 
                player.rect.y = level.second_teleporter.rect.y
                player.vel_y = 0
        except:
            pass





        # Draw
        win.fill(WHITE)
        level.background.set_background_image(level)

        level.platform_group.draw(win) #Draw Platforms
        try:
            level.teleporter_group.draw(win)
        except:
            pass

        level.background_group.draw(win)
        level.portal_group.draw(win)

        try:
            level.gurterade_group.draw(win) # Draw gurterade
        except:
            pass

        player_group.draw(win) #Draw player LAST

        #Things for testing (delete after full release)

        coor = FONT.render(f"Coordinates: {player.rect.x}, {player.rect.y}", True, (0, 0, 0))
        win.blit(coor, (700, 100))

        pygame.display.flip()  # Update the display


main()

#GUI:



pygame.quit()
sys.exit()
