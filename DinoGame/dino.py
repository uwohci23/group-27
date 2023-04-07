import os
import random
import threading

import pygame
from hand_control import *

pygame.init()

# Global Constants

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Game")

Ico = pygame.image.load("DinoGame/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("DinoGame/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("DinoGame/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("DinoGame/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("DinoGame/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("DinoGame/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("DinoGame/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("DinoGame/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("DinoGame/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("DinoGame/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("DinoGame/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("DinoGame/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("DinoGame/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("DinoGame/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("DinoGame/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("DinoGame/Other", "Track.png"))

FONT_COLOR=(0,0,0)

video = None
detector = None

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        global video,detector
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        check = get_label_hand("",video,detector)
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE] or check=="jump") and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif (userInput[pygame.K_DOWN] or check=="duck") and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

easy = True
medium = False
hard = False

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, light, dark, easy, medium, hard, video, detector
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("Royal Kingdom.ttf", 40)
    obstacles = []
    death_count = 0
    pause = False
    light = True
    dark = False
    
    if easy and not medium and not hard:
        game_speed = 15
    elif not easy and medium and not hard:
        game_speed = 20
    elif not easy and not medium and hard:
        game_speed = 30

    def score():
        global points, game_speed, light, dark
        points += 1
        if points % 75 == 0:
            game_speed += 2
            
        with open("DinoGame/score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            if light == True:
                FONT_COLOR = (0, 0, 0)
            else:
                FONT_COLOR = (255, 255, 255)
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)
        
        if easy and not medium and not hard:
            difficultyText = font.render("Difficulty: Easy", True, FONT_COLOR)
        elif not easy and medium and not hard:
            difficultyText = font.render("Difficulty: Medium", True, FONT_COLOR)
        elif not easy and not medium and hard:
            difficultyText = font.render("Difficulty: Hard", True, FONT_COLOR)
        difficultyTextRect = difficultyText.get_rect()
        difficultyTextRect.topleft = (30, 20)
        SCREEN.blit(difficultyText, difficultyTextRect)
        
        # Load and scale the settings button image
        if light == True:   
            settings_button_image = pygame.image.load("DinoGame/gearBlack.png")
        else:
            settings_button_image = pygame.image.load("DinoGame/gearWhite.png")
        settings_button_image = pygame.transform.scale(settings_button_image, (50, 50))

        # Draw the settings button at the top right corner of the screen
        button_rect = settings_button_image.get_rect()
        button_rect.topright = (SCREEN_WIDTH - 50, 15)
        SCREEN.blit(settings_button_image, button_rect)
        
        # help_font = pygame.font.Font("Royal Kingdom.ttf", 22)
        
        # helpText1 = help_font.render("1. Closed hand -> Run", True, FONT_COLOR)
        # helpTextRect1 = helpText1.get_rect()
        # helpTextRect1.bottomleft = (30, 580)
        # SCREEN.blit(helpText1, helpTextRect1)
        
        # helpText2 = help_font.render("2. Open palm (all 5 fingers up) -> Jump", True, FONT_COLOR)
        # helpTextRect2 = helpText2.get_rect()
        # helpTextRect2.bottomleft = (30, 620)
        # SCREEN.blit(helpText2, helpTextRect2)
        
        # helpText3 = help_font.render("3. Raise ONLY Index Finger -> Duck", True, FONT_COLOR)
        # helpTextRect3 = helpText3.get_rect()
        # helpTextRect3.bottomleft = (30, 660)
        # SCREEN.blit(helpText3, helpTextRect3)
        help_font = pygame.font.Font("Royal Kingdom.ttf", 44)

        # Load the closed hand image and resize it
        closed_hand_image = pygame.image.load("DinoGame/closed_hand.png")
        closed_hand_image = pygame.transform.scale(closed_hand_image, (help_font.get_height(), help_font.get_height()))
        
        open_palm_image = pygame.image.load("DinoGame/open_palm.png")
        open_palm_image = pygame.transform.scale(open_palm_image, (help_font.get_height(), help_font.get_height()))
        
        index_finger_image = pygame.image.load("DinoGame/index_finger.png")
        index_finger_image = pygame.transform.scale(index_finger_image, (help_font.get_height(), help_font.get_height()))

        # Render the help texts
        helpText1 = help_font.render("1. Run -> ", True, FONT_COLOR)
        helpText2 = help_font.render(", 2. Jump -> ", True, FONT_COLOR)
        helpText3 = help_font.render(", 3. Duck -> ", True, FONT_COLOR)

        # Get the rects for the help texts
        helpTextRect1 = helpText1.get_rect()
        helpTextRect2 = helpText2.get_rect()
        helpTextRect3 = helpText3.get_rect()

        # Set the positions of the help texts
        helpTextRect1.center = (100, 650)
        helpTextRect2.center = (320, 650)
        helpTextRect3.center = (560, 650)

        # Blit the help texts and the closed hand image
        SCREEN.blit(helpText1, helpTextRect1)
        SCREEN.blit(closed_hand_image, (helpTextRect1.right, helpTextRect1.y))
        SCREEN.blit(helpText2, helpTextRect2)
        SCREEN.blit(open_palm_image, (helpTextRect2.right, helpTextRect2.y))
        SCREEN.blit(helpText3, helpTextRect3)
        SCREEN.blit(index_finger_image, (helpTextRect3.right, helpTextRect3.y))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the settings button is clicked
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    paused()

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def showSettingsMenu():
        global button_font, profile_button_rect, themes_button_rect, close_button_rect, exit_button_rect
        
        # This function will display the small menu
        settings_image = pygame.image.load("DinoGame/settings.png")
        size = (500, 500)
        settings_image = pygame.transform.scale(settings_image, size)
        settings_rect = settings_image.get_rect()
        settings_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(settings_image, settings_rect)

        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 325
        button_height = 80
        button_padding = 40
        button_x = (SCREEN_WIDTH - button_width) // 2 + 10
        button_y = settings_rect.top + button_padding + 50

        # Themes button
        themes_button_text = button_font.render("Themes", True, FONT_COLOR)
        themes_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), themes_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), themes_button_rect, 2, border_radius=20)  # black border
        themes_button_text_rect = themes_button_text.get_rect(center=themes_button_rect.center)
        SCREEN.blit(themes_button_text, themes_button_text_rect)

        # How to play button
        button_y += button_height + button_padding
        profile_button_text = button_font.render("How to Play", True, FONT_COLOR)
        profile_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), profile_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), profile_button_rect, 2, border_radius=20)  # black border
        profile_button_text_rect = profile_button_text.get_rect(center=profile_button_rect.center)
        SCREEN.blit(profile_button_text, profile_button_text_rect)
        
        # Exit button
        button_y += button_height + button_padding
        exit_button_text = button_font.render("Exit", True, FONT_COLOR)
        exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), exit_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        SCREEN.blit(exit_button_text, exit_button_text_rect)
        
        # Close button
        close_button_rect = pygame.Rect(settings_rect.left + 50, settings_rect.top + 50, 50, 55)
        pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
        close_text = button_font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        SCREEN.blit(close_text, close_text_rect)

        pygame.display.update()

    def showThemes():
        global light, dark
        
        themes_image = pygame.image.load("DinoGame/settings.png")
        size = (500, 500)
        themes_image = pygame.transform.scale(themes_image, size)
        themes_rect = themes_image.get_rect()
        themes_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(themes_image, themes_rect)
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 180
        button_height = 180
        button_padding = 40
        button_x = (SCREEN_WIDTH - button_width) // 2 + 10
        button_y = themes_rect.top + button_padding + 200
        
        # Light themes button
        light_image = pygame.image.load("DinoGame/light.png")
        light_image = pygame.transform.scale(light_image, (button_width, button_height))
        light_button_rect = light_image.get_rect()
        light_button_rect.center = (button_x - 20, button_y - 20)
        SCREEN.blit(light_image, light_button_rect)
        
        # 'LIGHT' text
        light_text_surface = button_font.render('LIGHT', True, (255, 255, 255))
        light_text_rect = light_text_surface.get_rect()
        light_text_rect.midtop = (light_button_rect.centerx, light_button_rect.bottom + 5)
        SCREEN.blit(light_text_surface, light_text_rect)
        
        # Dark themes button
        dark_image = pygame.image.load("DinoGame/dark.png")
        dark_image = pygame.transform.scale(dark_image, (button_width, button_height))
        dark_button_rect = dark_image.get_rect()
        dark_button_rect.center = (button_x + 190, button_y - 20)
        SCREEN.blit(dark_image, dark_button_rect)
        
        # 'DARK' text
        dark_text_surface = button_font.render('DARK', True, (0, 0, 0))
        dark_text_rect = dark_text_surface.get_rect()
        dark_text_rect.midtop = (dark_button_rect.centerx, dark_button_rect.bottom + 5)
        SCREEN.blit(dark_text_surface, dark_text_rect)
        
        # Back button
        back_button_text = button_font.render("BACK", True, (0, 0, 0))
        back_button_rect = pygame.Rect(button_x, button_y + 180, button_width, 60)
        pygame.draw.rect(SCREEN, (255, 255, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        SCREEN.blit(back_button_text, back_button_text_rect)
        
        # Close button
        close_button_rect = pygame.Rect(themes_rect.left + 50, themes_rect.top + 50, 50, 55)
        pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
        close_text = button_font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        SCREEN.blit(close_text, close_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    unpause()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if light_button_rect.collidepoint(mouse_pos):
                        light = True
                        dark = False
                        unpause()
                        pygame.display.update()
                        return
                    elif dark_button_rect.collidepoint(mouse_pos):
                        light = False
                        dark = True
                        unpause()
                        pygame.display.update()
                        return
                    elif back_button_rect.collidepoint(mouse_pos):
                        paused()
                        pygame.display.update()
                        return
                    elif close_button_rect.collidepoint(mouse_pos):
                        unpause()
                        return
            
            pygame.display.update()
    
    def htpInGame():
        #text box
        text_box_image = pygame.image.load("DinoGame/settings.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create a font object
        text_font = pygame.font.Font("Royal Kingdom.ttf", 28)

        # Define the text to be rendered
        text_lines = [
            'The original version of the game ', 
            'had keyboard as the mode of input. ',
            'Our redesign focusses on ',
            'increasing this game\'s accessibility. ',
            '',
            'For playing the game with hand ',
            'gestures -',
            '1. Closed hand -> Run',
            '2. Open palm (all 5 fingers up) -> Jump',
            '3. Raise ONLY Index Finger -> Duck'
        ]

        # Render the text onto a surface
        text_surfaces = []
        max_line_width = 0  # Track the maximum line width
        for line in text_lines:
            text_surface = text_font.render(line, True, (255, 255, 255))
            text_surfaces.append(text_surface)
            line_width, line_height = text_font.size(line)
            max_line_width = max(max_line_width, line_width)

        # Calculate the height of the text box
        line_height = text_font.get_linesize()
        text_box_height = line_height * len(text_lines)

        # Create a new surface for the text box
        text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

        # Set the colorkey of the text box surface to be transparent
        text_box_surface.set_colorkey((0, 0, 0, 0))

        # Blit the text surfaces onto the text box surface
        for i, surface in enumerate(text_surfaces):
            text_box_surface.blit(surface, (0, i*line_height))

        # Blit the text box surface onto the screen
        SCREEN.blit(text_box_image, text_box_image_rect)
        SCREEN.blit(text_box_surface, (text_box_image_rect.left + 45, text_box_image_rect.top + 85))
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 30)
        button_width = 180
        button_height = 180
        button_padding = 40
        button_x = (SCREEN_WIDTH - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Back button
        back_button_text = button_font.render("BACK", True, (0, 0, 0))
        back_button_rect = pygame.Rect(button_x, button_y + 180, button_width, 50)
        pygame.draw.rect(SCREEN, (255, 255, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        SCREEN.blit(back_button_text, back_button_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    unpause()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        paused()
                        pygame.display.update()
                        return
        
            pygame.display.update()
    
    def exitGame():
        global video,detector
        #text box
        text_box_image = pygame.image.load("DinoGame/settings.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create a font object
        text_font = pygame.font.Font("Royal Kingdom.ttf", 40)

        # Define the text to be rendered
        text_lines = [
            'Are you sure you want ',
            'to return to the menu? ',
        ]

        # Render the text onto a surface
        text_surfaces = []
        max_line_width = 0  # Track the maximum line width
        for line in text_lines:
            text_surface = text_font.render(line, True, (255, 255, 255))
            text_surfaces.append(text_surface)
            line_width, line_height = text_font.size(line)
            max_line_width = max(max_line_width, line_width)

        # Calculate the height of the text box
        line_height = text_font.get_linesize()
        text_box_height = line_height * len(text_lines)

        # Create a new surface for the text box
        text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

        # Set the colorkey of the text box surface to be transparent
        text_box_surface.set_colorkey((0, 0, 0, 0))

        # Blit the text surfaces onto the text box surface
        for i, surface in enumerate(text_surfaces):
            text_box_surface.blit(surface, (0, i*line_height))

        # Blit the text box surface onto the screen
        SCREEN.blit(text_box_image, text_box_image_rect)
        SCREEN.blit(text_box_surface, (text_box_image_rect.left + 55, text_box_image_rect.top + 90))
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 180
        button_height = 120
        button_padding = 40
        button_x = (SCREEN_WIDTH - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Yes button
        yes_button_text = button_font.render("YES", True, FONT_COLOR)
        yes_button_rect = pygame.Rect(button_x - 115, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), yes_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), yes_button_rect, 2, border_radius=20)  # black border
        yes_button_text_rect = yes_button_text.get_rect(center=yes_button_rect.center)
        SCREEN.blit(yes_button_text, yes_button_text_rect)
        
        # No button
        no_button_text = button_font.render("NO", True, FONT_COLOR)
        no_button_rect = pygame.Rect(button_x + 105, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), no_button_rect, border_radius=20)
        pygame.draw.rect(SCREEN, (0, 0, 0), no_button_rect, 2, border_radius=20)  # black border
        no_button_text_rect = no_button_text.get_rect(center=no_button_rect.center)
        SCREEN.blit(no_button_text, no_button_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    unpause()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button_rect.collidepoint(mouse_pos):
                        kill_feed(video)
                        menu(death_count=0)
                        pygame.display.update()
                        return
                    elif no_button_rect.collidepoint(mouse_pos):
                        paused()
                        pygame.display.update()
                        return
        
            pygame.display.update()
        
    def paused():
        nonlocal pause
        pause = True
        showSettingsMenu()
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    unpause()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if themes_button_rect.collidepoint(mouse_pos):
                        showThemes()
                    elif profile_button_rect.collidepoint(mouse_pos):
                        htpInGame()
                    elif close_button_rect.collidepoint(mouse_pos):
                        unpause()
                    elif exit_button_rect.collidepoint(mouse_pos):
                        exitGame()

    while run:
        for event in pygame.event.get():
            check = get_label_hand('no_kill',video,detector)
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or check == 'no_hand':
                run = False
                paused()
                
        if light == True:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                kill_feed(video)
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    global FONT_COLOR
    run = True
    
    while run:
        
        def mainMenu():
            
            wallpaper_image = pygame.image.load("DinoGame/DinoWallpaper.png")
            wallpaper_image_rect = wallpaper_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 240))
            SCREEN.blit(wallpaper_image, wallpaper_image_rect)
            
            if death_count == 0:
                name = font.render("Chrome Dino Game", True, FONT_COLOR)
                nameRect = name.get_rect()
                nameRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
                SCREEN.blit(name, nameRect)
                # mainMenu()
                
            elif death_count > 0:
                score = font.render("Your Score: " + str(points), True, FONT_COLOR)
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170)
                SCREEN.blit(score, scoreRect)
                f = open("DinoGame/score.txt", "a")
                f.write(str(points) + "\n")
                f.close()
                with open("DinoGame/score.txt", "r") as f:
                    score = (
                        f.read()
                    )  # Read all file in case values are not on a single line
                    score_ints = [int(x) for x in score.split()]  # Convert strings to ints
                highscore = max(score_ints)  # sum all elements of the list
                hs_score_text = font.render(
                    "High Score : " + str(highscore), True, FONT_COLOR
                )
                hs_score_rect = hs_score_text.get_rect()
                hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  - 120)
                SCREEN.blit(hs_score_text, hs_score_rect)
        
            # draw buttons
            button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
            button_width = 350
            button_height = 80
            button_padding = 40
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y = SCREEN_HEIGHT // 2 - button_height

            # New Game button
            game_button_text = button_font.render("New Game", True, (255, 255, 255))
            game_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (113, 112, 110, 255), game_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), game_button_rect, 2, border_radius=20)  # black border
            game_button_text_rect = game_button_text.get_rect(center=game_button_rect.center)
            SCREEN.blit(game_button_text, game_button_text_rect)

            # Help button
            button_y += button_height + button_padding
            help_button_text = button_font.render("Help", True, (255, 255, 255))
            help_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (113, 112, 110, 255), help_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), help_button_rect, 2, border_radius=20)  # black border
            help_button_text_rect = help_button_text.get_rect(center=help_button_rect.center)
            SCREEN.blit(help_button_text, help_button_text_rect)
            
            # Exit button
            button_y += button_height + button_padding
            exit_button_text = button_font.render("Exit", True, (255, 255, 255))
            exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (113, 112, 110, 255), exit_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
            exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
            SCREEN.blit(exit_button_text, exit_button_text_rect)
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if game_button_rect.collidepoint(mouse_pos):
                            setDifficulty()
                            # startGame()     
                            # main()
                        elif help_button_rect.collidepoint(mouse_pos):
                            showHelp()
                        elif exit_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            os.system('python launcher.py')
                            quit()               
                
                pygame.display.update()
        
        def setDifficulty():
            global easy, medium, hard
            
            # This function will display the small menu
            difficulty_image = pygame.image.load("DinoGame/settings.png")
            size = (500, 500)
            difficulty_image = pygame.transform.scale(difficulty_image, size)
            difficulty_rect = difficulty_image.get_rect()
            difficulty_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(difficulty_image, difficulty_rect)
            
            difficulty = pygame.font.Font("Royal Kingdom.ttf", 55).render("Set Difficulty", True, FONT_COLOR)
            difficultyRect = difficulty.get_rect()
            difficultyRect.center = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 120)
            SCREEN.blit(difficulty, difficultyRect)

            # draw buttons
            button_font = pygame.font.Font("Royal Kingdom.ttf", 45)
            button_width = 325
            button_height = 60
            button_padding = 40
            button_x = (SCREEN_WIDTH - button_width) // 2 + 10
            button_y = difficulty_rect.top + button_padding + 150

            # Easy button
            easy_button_text = button_font.render("Easy", True, FONT_COLOR)
            easy_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), easy_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), easy_button_rect, 2, border_radius=20)  # black border
            easy_button_text_rect = easy_button_text.get_rect(center=easy_button_rect.center)
            SCREEN.blit(easy_button_text, easy_button_text_rect)

            # Medium button
            button_y += button_height + button_padding
            medium_button_text = button_font.render("Medium", True, FONT_COLOR)
            medium_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), medium_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), medium_button_rect, 2, border_radius=20)  # black border
            medium_button_text_rect = medium_button_text.get_rect(center=medium_button_rect.center)
            SCREEN.blit(medium_button_text, medium_button_text_rect)
            
            # Hard button
            button_y += button_height + button_padding
            hard_button_text = button_font.render("Hard", True, FONT_COLOR)
            hard_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), hard_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), hard_button_rect, 2, border_radius=20)  # black border
            hard_button_text_rect = hard_button_text.get_rect(center=hard_button_rect.center)
            SCREEN.blit(hard_button_text, hard_button_text_rect)
            
            # Close button
            close_button_rect = pygame.Rect(difficulty_rect.left + 50, difficulty_rect.top + 50, 50, 55)
            pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
            close_text = button_font.render("X", True, (255, 255, 255))
            close_text_rect = close_text.get_rect(center=close_button_rect.center)
            SCREEN.blit(close_text, close_text_rect)
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                        mainMenu()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if easy_button_rect.collidepoint(mouse_pos):
                            print('easy')
                            easy = True
                            medium = False
                            hard = False
                            startGame()
                        elif medium_button_rect.collidepoint(mouse_pos):
                            print('medium')
                            easy = False
                            medium = True
                            hard = False
                            startGame()
                        elif hard_button_rect.collidepoint(mouse_pos):
                            print('hard')
                            easy = False
                            medium = False
                            hard = True
                            startGame()
                        elif close_button_rect.collidepoint(mouse_pos):
                            menu(death_count=0)

                pygame.display.update()
            
        def startGame():
            global video, detector, easy, medium, hard
            clock = pygame.time.Clock()
            counter, text = 6, 'Starting in...'
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            
            
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT: 
                        counter -= 1
                        if counter > 0 :
                            text = str(counter)
                        else:
                            video,detector = initializer()
                            main()
                    if event.type == pygame.QUIT: 
                        run = False
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                        menu(death_count=0)
                    

                # SCREEN.fill((255, 255, 255))
                background_image = pygame.image.load('DinoGame/homeBackground.png').convert()
                background_image = pygame.transform.scale(background_image, (1280, 700))
                SCREEN.blit(background_image, (0, 0))
                font = pygame.font.Font("Royal Kingdom.ttf", 55)
                
                name1 = font.render("Place your hand in front of the camera", True, FONT_COLOR)
                name1Rect = name1.get_rect()
                name1Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125)
                SCREEN.blit(name1, name1Rect)
                
                name2 = font.render("Or press Esc to go back to menu", True, FONT_COLOR)
                name2Rect = name2.get_rect()
                name2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 55)
                SCREEN.blit(name2, name2Rect)
                
                timer = font.render(text, True, FONT_COLOR)
                timerRect = timer.get_rect()
                timerRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5)
                SCREEN.blit(timer, timerRect)
                pygame.display.flip()
                clock.tick(60)
                
            
            pygame.display.update()
            
        def showHelp():
            background_image = pygame.image.load('DinoGame/homeBackground.png').convert()
            background_image = pygame.transform.scale(background_image, (1280, 700))
            background_image_rect = background_image.get_rect()
            background_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(background_image, background_image_rect)
            
            # draw buttons
            button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
            button_width = 425
            button_height = 80
            button_padding = 40
            button_x = (SCREEN_WIDTH - button_width) // 2 - 325
            button_y = SCREEN_HEIGHT // 2 - button_height

            # About Game button
            about_game_button_text = button_font.render("About Game", True, (0, 0, 0))
            about_game_button_rect = pygame.Rect(button_x, button_y - 70, button_width, button_height)
            pygame.draw.rect(SCREEN, (113, 112, 110, 255), about_game_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), about_game_button_rect, 2, border_radius=20)  # black border
            about_game_button_text_rect = about_game_button_text.get_rect(center=about_game_button_rect.center)
            SCREEN.blit(about_game_button_text, about_game_button_text_rect)

            # How to play button
            button_y += button_height + button_padding
            htp_button_text = button_font.render("How To Play", True, (0, 0, 0))
            htp_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (255, 255, 255, 255), htp_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), htp_button_rect, 2, border_radius=20)  # black border
            htp_button_text_rect = htp_button_text.get_rect(center=htp_button_rect.center)
            SCREEN.blit(htp_button_text, htp_button_text_rect)

            # Back button
            back_button_text = button_font.render("BACK", True, (0, 0, 0))
            back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - button_height + 350, 180, 60)
            pygame.draw.rect(SCREEN, (255, 255, 255), back_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
            back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
            SCREEN.blit(back_button_text, back_button_text_rect)
            
            # #text box
            text_box_image = pygame.image.load("DinoGame/settings.png")
            size = (650, 550)
            text_box_image = pygame.transform.scale(text_box_image, size)
            text_box_image_rect = text_box_image.get_rect()
            text_box_image_rect.center = (SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 - 50)
            
            # Create a font object
            text_font = pygame.font.Font("Royal Kingdom.ttf", 30)

            # Define the text to be rendered
            text_lines = [
                'Chrome Dino is a game that was created by ',
                'the Google Chrome team in 2014. The game ',
                'was designed as an Easter egg to entertain ',
                'users when they experience connectivity ',
                'issues and the Chrome browser displays a ',
                '"No Internet" error page.',
                '',
                'The idea for the game came from a team of ',
                'Chrome developers who wanted to create a ',
                'fun and engaging game that users could ',
                'play while waiting for their internet ',
                'connection to be restored.'
            ]

            # Render the text onto a surface
            text_surfaces = []
            max_line_width = 0  # Track the maximum line width
            for line in text_lines:
                text_surface = text_font.render(line, True, (255, 255, 255))
                text_surfaces.append(text_surface)
                line_width, line_height = text_font.size(line)
                max_line_width = max(max_line_width, line_width)

            # Calculate the height of the text box
            line_height = text_font.get_linesize()
            text_box_height = line_height * len(text_lines)

            # Create a new surface for the text box
            text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

            # Set the colorkey of the text box surface to be transparent
            text_box_surface.set_colorkey((0, 0, 0, 0))

            # Blit the text surfaces onto the text box surface
            for i, surface in enumerate(text_surfaces):
                text_box_surface.blit(surface, (0, i*line_height))

            # Blit the text box surface onto the screen
            SCREEN.blit(text_box_image, text_box_image_rect)
            SCREEN.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 95))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if about_game_button_rect.collidepoint(mouse_pos):
                            pass
                        elif htp_button_rect.collidepoint(mouse_pos):
                            howToPlay()
                            pygame.display.update()
                            return
                        elif back_button_text_rect.collidepoint(mouse_pos):
                            menu(death_count)
                            return                  
                
                pygame.display.update()
        
        def howToPlay():
            background_image = pygame.image.load('DinoGame/homeBackground.png').convert()
            background_image = pygame.transform.scale(background_image, (1280, 700))
            background_image_rect = background_image.get_rect()
            background_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(background_image, background_image_rect)
            
            # draw buttons
            button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
            button_width = 425
            button_height = 80
            button_padding = 40
            button_x = (SCREEN_WIDTH - button_width) // 2 - 325
            button_y = SCREEN_HEIGHT // 2 - button_height

            # About Game button
            about_game_button_text = button_font.render("About Game", True, (0, 0, 0))
            about_game_button_rect = pygame.Rect(button_x, button_y - 70, button_width, button_height)
            pygame.draw.rect(SCREEN, (255, 255, 255, 255), about_game_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), about_game_button_rect, 2, border_radius=20)  # black border
            about_game_button_text_rect = about_game_button_text.get_rect(center=about_game_button_rect.center)
            SCREEN.blit(about_game_button_text, about_game_button_text_rect)

            # How to play button
            button_y += button_height + button_padding
            htp_button_text = button_font.render("How To Play", True, (0, 0, 0))
            htp_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(SCREEN, (113, 112, 110, 255), htp_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), htp_button_rect, 2, border_radius=20)  # black border
            htp_button_text_rect = htp_button_text.get_rect(center=htp_button_rect.center)
            SCREEN.blit(htp_button_text, htp_button_text_rect)

            # Back button
            back_button_text = button_font.render("BACK", True, (0, 0, 0))
            back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - button_height + 350, 180, 60)
            pygame.draw.rect(SCREEN, (255, 255, 255), back_button_rect, border_radius=20)
            pygame.draw.rect(SCREEN, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
            back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
            SCREEN.blit(back_button_text, back_button_text_rect)
            
            #text box
            text_box_image = pygame.image.load("DinoGame/settings.png")
            size = (650, 550)
            text_box_image = pygame.transform.scale(text_box_image, size)
            text_box_image_rect = text_box_image.get_rect()
            text_box_image_rect.center = (SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 - 50)
            
            # Create a font object
            text_font = pygame.font.Font("Royal Kingdom.ttf", 35)

            # Define the text to be rendered
            text_lines = [
                'The original version of the game had ', 
                'keyboard as the mode of input. Our ',
                'redesign focusses on increasing this ',
                'game\'s accessibility. ',
                '',
                'For playing the game with hand ',
                'gestures -',
                '1. Closed hand -> Run',
                '2. Open palm (all 5 fingers up) -> Jump',
                '3. Raise ONLY Index Finger -> Duck'
            ]

            # Render the text onto a surface
            text_surfaces = []
            max_line_width = 0  # Track the maximum line width
            for line in text_lines:
                text_surface = text_font.render(line, True, (255, 255, 255))
                text_surfaces.append(text_surface)
                line_width, line_height = text_font.size(line)
                max_line_width = max(max_line_width, line_width)

            # Calculate the height of the text box
            line_height = text_font.get_linesize()
            text_box_height = line_height * len(text_lines)

            # Create a new surface for the text box
            text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

            # Set the colorkey of the text box surface to be transparent
            text_box_surface.set_colorkey((0, 0, 0, 0))

            # Blit the text surfaces onto the text box surface
            for i, surface in enumerate(text_surfaces):
                text_box_surface.blit(surface, (0, i*line_height))

            # Blit the text box surface onto the screen
            SCREEN.blit(text_box_image, text_box_image_rect)
            SCREEN.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 95))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        if about_game_button_rect.collidepoint(mouse_pos):
                            showHelp()
                            pygame.display.update()
                            return
                        elif htp_button_rect.collidepoint(mouse_pos):
                            pass
                        elif back_button_text_rect.collidepoint(mouse_pos):
                            menu(death_count)
                            return                  
                
                pygame.display.update()
            
        FONT_COLOR=(0,0,0)
        # SCREEN.fill((255, 255, 255))
        font = pygame.font.Font("Royal Kingdom.ttf", 40)
        background_image = pygame.image.load('DinoGame/homeBackground.png').convert()
        background_image = pygame.transform.scale(background_image, (1280, 700))
        SCREEN.blit(background_image, (0, 0))
        mainMenu()
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()