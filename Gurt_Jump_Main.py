#Coding notes: we should program stuff in linear progression of the game
#This meaning like we program everything for level 1 first, then everything for level 2, and so on

#Importing Functions
import pygame
import random
import math
import sys
import tkinter as tk
from tkinter import messagebox



pygame.init()

#Game setup:
WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GURT JUMP WOOOOOOO! Level: " )
FPS = 30
clock = pygame.time.Clock()

GREEN = (50, 205, 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)

#Various Global Variables
Player_Width = 32
Player_Height = 32
Player_Speed = 20
Jump_Strength = -20
Gravity = 1



#Classes

class GameObject:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._width = 32 # To be over-riden
        self._height = 32 # To be over-riden

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self._x, self._y, self._width, self._height)) #to be over-riden

    def get_position(self):
        return self._x, self._y



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((Player_Width, Player_Height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False

    # Edit this so velocity slowly increases as you hold BUT CAPS OUT AT A MAX VELOCITY
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
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
                if self.vel_y < 0:
                    self.vel_y = 0
                    self.rect.top = platform.rect.bottom





class Spikes(GameObject):
    pass



class FakeCheckpoint(GameObject):
    pass



class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)



class Gurterade(Portal):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(PURPLE) #Replace with the actual image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN) #Replace with the actual image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)





class Teleporter(GameObject): # going to delay this until like the end probably
    pass



class Jumppad(GameObject): 
    pass



class Level:
    def __init__(self):
        self.current_level = 1
        self.platforms = []
        self.platform_group = pygame.sprite.Group()
        self.portal = None
        self.lava = None
        self.gurterade = None
        self.load_level()

    def load_level(self):
        self.platforms = []
        if self.current_level == 1:
            #Platform(X, Y, Height, Width)
            self.platforms = [ #Placeholder variables
                Platform(0, HEIGHT - 20, WIDTH, 20),
                Platform(500, 700, 100, 20),
                Platform(700, 575, 120, 20)

            ]
            self.portal = Portal(850, 550, 75, 75)
            self.gurterade = Gurterade (800, 350, 50, 50)

        if self.current_level == 2:
            #Platform(X, Y, Height, Width)
            self.platforms = [ #Placeholder variables
                Platform(0, HEIGHT - 20, WIDTH, 20),
                Platform(400, 600, 100, 20),
                Platform(300, 475, 120, 20)

            ]
            self.portal = Portal(850, 550, 75, 75)

        self.platform_group = pygame.sprite.Group((self.platforms) + [self.portal] + [self.gurterade])

    
    def next_level(self):
        self.current_level += 1
        self.load_level()





#Game
def main():
    player = Player(100, HEIGHT - Player_Height - 100) #This will be over-riden and maybe deleted 
    player_group = pygame.sprite.Group(player)
    
    gerteradeCollected = False

    level = Level()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player_group.update(level.platforms) #Update player

        if level.gurterade.check_collision(player):
            gerteradeCollected = True # Update later to work

        if gerteradeCollected == True:
            if level.portal.check_collision(player):
                player.rect.x = 100
                player.rect.y = 500
                player.vel_y = 0
                gerteradeCollected = False
                level.next_level()


        # Draw
        win.fill(WHITE)
        player_group.draw(win) #Draw player
        level.platform_group.draw(win) #Draw Platforms
        pygame.display.flip()  # Update the display


main()

#GUI:



pygame.quit()
sys.exit()



