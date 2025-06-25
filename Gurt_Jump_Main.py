#Coding notes: we should program stuff in linear progression of the game
#This meaning like we program everything for level 1 first, then everything for level 2, and so on
#place the py file in gurt file
#Importing Functions
import pygame
import sys



pygame.init()

#Game setup:
WIDTH, HEIGHT = 1024, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"GURT JUMP WOOOOOOO! Level: ")
FONT = pygame.font.SysFont("comisans", 40)
FPS = 30
clock = pygame.time.Clock()

#Various placeholder colours
GREEN = (50, 205, 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
ORANGE = (100, 64, 0)
LIGHT_BLUE = (173, 216, 230)
MAGENTA = (255, 0, 255)
BLACK = (255, 255, 255)

#Various Global Variables
Player_Speed = 20
Jump_Strength = -20
Gravity = 1



#Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("the gurt.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
        self.teleport_cooldown = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = self.vel_y

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.dx -= Player_Speed
        if keys[pygame.K_RIGHT] and self.rect.x < 1024 - 64:
            self.dx += Player_Speed
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = Jump_Strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += Gravity
        self.dy = self.vel_y

        # Horizontal movement and collision
        self.rect.x += self.dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.dx > 0:  # Moving right; Hit the left side of the platform
                    self.rect.right = platform.rect.left
                if self.dx < 0:  # Moving left; Hit the right side of the platform
                    self.rect.left = platform.rect.right

        # Vertical movement and collision
        self.rect.y += self.dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        if self.rect.y < 0: # Makes sure you can't go 'above' the screen
            self.vel_y = 0
            self.rect.y = 0

    def Player_Respawn(self, level): #Simple code to respawn the player, also called when player gets to the next level
        if level.current_level == 1:
            self.rect.x = 10
            self.rect.y = 10
            self.vel_y = 0
            self.dx = 0
        if level.current_level == 2:
            self.rect.x = 100
            self.rect.y = 540
            self.vel_y = 0
            self.dx = 0
        if level.current_level == 3:
            self.rect.x = 218
            self.rect.y = 58
            self.vel_y = 0
            self.dx = 0
        if level.current_level == 4:
            self.rect.x = 30
            self.rect.y = 30
            self.vel_y = 0
            self.dx = 0



class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("level 1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_background_image(self, level): # Sets the background image depending on what level
        # We have a background image, which includes platforms and such, instead of individual sprites, because it is easier and less resource intensive
        if level.current_level == 1:
            self.image = pygame.image.load("level 1.png")
        if level.current_level == 2:
            self.image = pygame.image.load("level 2.png")
        if level.current_level == 3:
            self.image = pygame.image.load("level 3.png")
        if level.current_level == 4:
            self.image = pygame.image.load("level 4.png")

        return self.image




class Portal(pygame.sprite.Sprite): # The portal to the next level
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load("checkpoint.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)



class Gurterade(Portal): # The gurterade/key for the level
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load("gurtarade.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Spikes(pygame.sprite.Sprite): # This, and the next few classes are repetitive. They are mostly for functions that are defined in the game loop
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class First_Teleporter(Portal): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Second_Teleporter(Portal): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        #self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Jumppad(Portal): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface((width, height))
        #self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class Level: # The level!
    def __init__(self):
        self.current_level = 1 # The most important variable, depending on its value, we draw and make a different level. Once it reaches 5, game is won.
        self.platforms = []
        self.platform_group = pygame.sprite.Group()
        self.portal = None
        self.gurterade = None
        self.spikes = []
        self.first_teleporter = None
        self.second_teleporter = None
        self.background = None
        self.jumppads = []
        self.load_level()
        self.gerteradeCollected = False
      
    def load_level(self): # Loads the level, first by settting variables back to default, then making them again to 'craft' the level
        self.platforms = []
        self.spikes = []
        self.gurterade = None
        self.first_teleporter = None
        self.second_teleporter = None
        self.gerteradeCollected = False
        self.jumppads = []
        if self.current_level == 1:
            #(X, Y, Width, Height)
            self.platforms = [ 
                Platform(294, 291, 280, 48),
                Platform(587, 457, 327, 48),
                Platform(59, 552, 327, 48),
                Platform(0, 100, 270, 233),
                Platform(270, 150, 15, 100)
            ]
            self.spikes = [
                Spikes(-1000,740, 10240, 10) #This spike is to kill the player when they "fall out of the map."
            ]
            self.portal = Portal(300-50, 552-63, 64, 64)
            self.gurterade = Gurterade(800, 350, 64, 64)
            self.first_teleporter = First_Teleporter(903, 312, 81, 138)
            self.second_teleporter = Second_Teleporter(9, 349, 100, 135)
            self.background = Background(0,0, 1080, 720)

        if self.current_level == 2:
            #(X, Y, Width, Height)
            self.platforms = [ 
                Platform(0, 604, 175, 48),
                Platform(26, 265, 300, 48),
                Platform(163, 463, 300, 48),
                Platform(493, 341, 300, 48),
                Platform(876, 620, 300, 48)
            ]
            self.spikes = [
                Spikes(-1000, 740, 102400, 10) #This spike is to kill the player when they "fall out of the map."
            ]
            self.portal = Portal(903, 556, 64, 64)
            self.gurterade = Gurterade(80, 202, 64, 64)
            self.background = Background(0,0, 1080, 720)

        if self.current_level == 3:
            #(X, Y, Width, Height)
            self.platforms = [ 
                Platform(148, 122, 306, 49),
                Platform(405, 1, 46, 167),
                Platform(-1, 475, 280, 50),
                Platform(279, 384, 179, 43),
                Platform(424, 289, 297, 55),
                Platform(727, 319, 300, 49),
                Platform(393, 598, 301, 52),
                Platform(787, 627, 294, 52),
            ]
            self.portal = Portal(850, 550, 64, 64)
            self.spikes = [
                Spikes(-1000, 740, 102400, 10), #This spike is to kill the player when they "fall out of the map."
                Spikes(373, -3, 32, 120),
                Spikes(746, 268, 307, 51),
                Spikes(367, 330, 53, 57),
                Spikes(101, 424, 52, 51),
                
                        ]
            self.gurterade = Gurterade(800, 350, 64, 64)
            self.background = Background(0,0, 1080, 720)
            self.first_teleporter = First_Teleporter(693, 128, 92, 147)
            self.second_teleporter = Second_Teleporter(331, 457, 108, 140)

        if self.current_level == 4:
            #Platform(X, Y, Width, Height)
            self.platforms = [
                Platform(0, 103, 274, 48),
                Platform(0, 542, 274, 48),
                Platform(230, 421, 48, 165),
                Platform(315, 381, 305, 48),
                Platform(574, 261, 48, 165),
                Platform(859, 0, 48, 340),
                Platform(906, 36, 120, 48),
                Platform(760, 654, 300, 48)
            ]
            self.spikes = [
                Spikes(-1000, 740, 102400, 10), #This spike is to kill the player when they "fall out of the map."
                Spikes(154, 325, 54, 75),
                Spikes(168, 302, 26, 107),
                Spikes(385, 200, 59, 54),
                Spikes(398, 175, 29, 108),
                Spikes(760, 314, 50, 51),
                Spikes(770, 286, 30, 107),
                Spikes(239, 149, 57, 55),
                Spikes(214, 162, 107, 29)
            ]
            self.portal = Portal(910, 120, 64, 64)
            self.gurterade = Gurterade(80, 302, 64, 64)
            self.background = Background(0,0, 1080, 720)
            self.jumppads = [
                Jumppad(948, 637, 70, 22),
                Jumppad(504, 361, 70, 22),
                Jumppad(71, 527, 70, 22)
            ]
            self.first_teleporter = First_Teleporter(31, 162, 150, 64)
            self.second_teleporter = Second_Teleporter(684, 464, 148, 40)

        #Hashed out code kept incase future expansion happens

        #if self.jumppads:
            #self.platform_group = pygame.sprite.Group((self.platforms) + (self.jumppads) + (self.spikes))
        #else:
            #self.platform_group = pygame.sprite.Group((self.platforms) + (self.spikes))
        #if self.first_teleporter and self.second_teleporter:
            #self.teleporter_group = pygame.sprite.Group([self.first_teleporter] + [self.second_teleporter])
        #else:
            #self.teleporter_group = None
        
        #Needed to draw the sprites
        self.portal_group = pygame.sprite.Group(self.portal)
        if self.gurterade: # Only makes the group if gurterade exists (kinda useless but might do something with it later)
            self.gurterade_group = pygame.sprite.Group(self.gurterade)
        self.background_group = pygame.sprite.Group(self.background)
 
    def next_level(self, player): # Sets the level to the next one, and also forces the player to respawn
        self.current_level += 1
        player.Player_Respawn(self)

        self.load_level()

    def get_current_level(self): #Get function. We should've used more.
        return self.current_level





#Game
def game():

    player = Player(10, 10) #Create player
    player_group = pygame.sprite.Group(player)

    #Timer init
    timer_font = pygame.font.SysFont("comisans", 40)
    timer_sec = 60
    timer_text = timer_font.render("01:00", True, (0, 0, 0))
    timer = pygame.USEREVENT + 1                                                
    pygame.time.set_timer(timer, 1000)

    #Make the level, and set variables
    level = Level()
    won_game = False
    lost_game = False
    running = True

    while running:
        clock.tick(FPS)

        level_current = level.get_current_level()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == timer:    # checks for timer event
                if timer_sec > 0:
                    timer_sec -= 1
                    timer_text = timer_font.render(f"00:{timer_sec:02d}", True, (0, 0, 0))
                    if timer_sec == 0:
                        lost_game = True
                        running = False
                        break
                else:
                    pygame.time.set_timer(timer, 0)    # turns off timer event


        if level_current == 5: # Code that serves the GUI. This makes it so once you get to level 5, you win, but the display will say you beat level 4.
            won_game = True
            level_current -= 1
            running = False
            break
        

        player_group.update(level.platforms) #Update player

        for spike in level.spikes: # Kill player if they touch spikes
            if player.rect.colliderect(spike.rect): 
                level.load_level()
                player.Player_Respawn(level)

        if level.gurterade.check_collision(player):
            level.gerteradeCollected = True 
            level.gurterade.rect.topleft = (965,-10) # Moves the Gurterade

        if level.gerteradeCollected == True: # Checks to see if player collides with goal only when gurterade collected
            if level.portal.check_collision(player):
                level.next_level(player)


        # We use a cooldown so that the player isnt soft locked
        if player.teleport_cooldown > 0:
            player.teleport_cooldown -= 1

        try:
            if level.first_teleporter and level.second_teleporter:
                if player.teleport_cooldown == 0:
                    if level.first_teleporter.check_collision(player):
                        player.rect.x = level.second_teleporter.rect.x + 10
                        player.rect.y = level.second_teleporter.rect.y + 10
                        player.vel_y = 0
                        player.teleport_cooldown = FPS # = to fps so it stays the same in seconds if we edit fps 
                    elif level.second_teleporter.check_collision(player):
                        player.rect.x = level.first_teleporter.rect.x + 10
                        player.rect.y = level.first_teleporter.rect.y + 10
                        player.vel_y = 0
                        player.teleport_cooldown = FPS 
        except:
            pass
        
        for jumppad in level.jumppads:
            try:
                if jumppad.check_collision(player):
                    player.vel_y += (Jump_Strength * 5) # This logic can easily be changed to edit the jump pad's strength. Another way would be to do it in the level class to make it level specific (or do the same in the jumppad class)
                    player.on_ground = False
            except:
                pass

        # Draw the screen
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

        #coor = FONT.render(f"Coordinates: {player.rect.x}, {player.rect.y}", True, (0, 0, 0))
        #win.blit(coor, (700, 100))
        
        win.blit(timer_text, (900, 10))

        pygame.display.flip()  # Update the display
        pygame.display.set_caption(f"Gurt Jump level: {level_current}")

    return level_current, won_game, lost_game, timer_sec


def main(): # The main function
    gui_launch_page() # "Main menu GUI"
    play_game = True # Sets it up so that when you press space in the other gui's, it will play the game again
    while play_game == True:
        level_current, won_game, lost_game, timer_sec = game()
        if lost_game == True:
            gui_lost_the_game(level_current, play_game)
        elif won_game == True:
            gui_won_the_game(timer_sec)




#GUI:
def gui_launch_page():

    running = True
    pygame.display.set_caption("Welcome to Gurt Jump!") # Set display


    while running:
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # Check to see if player presses space
                if event.key == pygame.K_SPACE:
                    running = False

        # Text setup
        hello_text = FONT.render("Welcome to Gurt Jump.", True, (0, 0, 0)) 
        keybinds_text = FONT.render("To move, use the arrow keys.", True, (0, 0, 0))
        amount_of_time_text = FONT.render("You have one minute to beat the game.", True, (0, 0, 0))
        Gurterade_text = FONT.render("Get the gurterade to unlock the portal to the next level!", True, (0, 0, 0))
        avoid_the_spikes_text = FONT.render("Make sure to avoid the spikes!", True, (0, 0, 0))
        four_levels_text = FONT.render("There are four levels to beat.", True, (0, 0, 0))
        space_to_start_text = FONT.render("Press space to start!", True, (0, 0, 0))
        good_luck_text = FONT.render("Good luck!", True, (0, 0, 0))

        # Text rendering
        win.blit(hello_text, (100, 100))
        win.blit(keybinds_text, (100, 150))
        win.blit(amount_of_time_text, (100, 200))
        win.blit(Gurterade_text, (100, 250))
        win.blit(avoid_the_spikes_text, (100, 300))
        win.blit(four_levels_text, (100, 350))
        win.blit(space_to_start_text, (100, 400))
        win.blit(good_luck_text, (100, 450))

        pygame.display.flip()



def gui_lost_the_game(level_current, play_game):
    
    running = True
    play_game = False
    pygame.display.set_caption(f"Lost on level {level_current}")

    while running:
        win.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # Checks if player presses space
                if event.key == pygame.K_SPACE:
                    play_game = True
                    running = False

        # Text setup
        you_lost_text = FONT.render("You lost :(", True, (0, 0, 0))
        on_level_x_text = FONT.render(f"You got up to level: {level_current}", True, (0, 0, 0))
        try_not_hitting_spikes_text = FONT.render("Try not hiting the spikes this time you fool!", True, (0,0,0))
        press_space_text = FONT.render("Press space to try again!", True, (0,0,0))

        # Text render
        win.blit(you_lost_text, (100, 100))
        win.blit(on_level_x_text, (100,150))
        win.blit(try_not_hitting_spikes_text, (100, 200))
        win.blit(press_space_text, (100, 250))

        pygame.display.flip()

    return play_game 



def gui_won_the_game(timer_sec):
    
    running = True
    play_game = False
    time_to_beat = (timer_sec - 60) * -1 # Makes it so that the time to beat is how long it took rather than how long is left
    pygame.display.set_caption(f"Won in {time_to_beat} seconds!")

    while running:
        win.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_game = True
                    running = False

        # Text setup
        you_won_text = FONT.render("You WON!!!", True, (0,0,0))
        time_text = FONT.render(f"It took you: {time_to_beat} seconds!", True, (0,0,0))
        want_to_text = FONT.render("Want to try to beat your time?", True, (0,0,0))
        press_space_text = FONT.render("Press space to try again!", True, (0,0,0))
        good_luck_text = FONT.render("Good Luck!", True, (0,0,0))

        # Text rendering
        win.blit(you_won_text, (100,100))
        win.blit(time_text, (100,150))
        win.blit(want_to_text, (100, 200))
        win.blit(press_space_text, (100,250))
        win.blit(good_luck_text, (100, 300))

        pygame.display.flip()


    return play_game

#Call main function
main()

pygame.quit()
sys.exit()
main()

pygame.quit()
sys.exit()
