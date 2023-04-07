import pygame,sys;
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
import os
import menu
import time 



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

    def animate(self):
        self.current_frame += 1
        if self.current_frame == len(self.frames):
            self.current_frame = 0
        self.image = self.frames[self.current_frame]



class Game:
    def __init__(self,screen,theme='light'):
        self.max_level =1   
        self.screen = screen

        #plauyer attributes
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        self.theme = theme

        #audio
        self.level_bg_music = pygame.mixer.Sound('./Mario/audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound('./Mario/audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.3)

        #user interface
        self.run_level_check = False
        self.ui = UI(self.screen)

        #overworld creation
        self.overworld = Overworld(0,self.max_level,self.screen, self.create_level,self.create_overworld)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
        self.back_icon = pygame.image.load("./Mario/graphics/back_button.png").convert_alpha()
        self.back_rect = self.back_icon.get_rect(topleft = (0,0))


        font_helper = pygame.font.Font("Royal Kingdom.ttf",25)
        font_helper_use = pygame.font.Font("Royal Kingdom.ttf",35)
        self.use_key_text = font_helper_use.render("USE", True,(0,0,0))
        

        self.space_key = pygame.image.load("Mario/graphics/keyPress/space.png").convert_alpha()
        self.space_key_rect = self.space_key.get_rect(topleft = (300,40))

        self.space_key_text = font_helper.render("Enter Level", True,(0,0,0))
        self.space_key_text_rect = self.space_key_text.get_rect(topleft = (300+(self.space_key_rect.width+20),60))


        self.left_arrow_key = pygame.image.load("Mario/graphics/keyPress/leftArrow.png").convert_alpha()
        self.left_arrow_key_rect = self.left_arrow_key.get_rect(topleft = (550,40))
        
        
        self.right_arrow_key = pygame.image.load("Mario/graphics/keyPress/rightArrow.png").convert_alpha()
        self.right_arrow_key_rect = self.right_arrow_key.get_rect(topleft = (550+(self.left_arrow_key_rect.width+20),40))

        self.arrow_key_text = font_helper.render("Move between Levels", True, (0,0,0))
        self.arrow_key_text_rect = self.arrow_key_text.get_rect(topleft = (550+(self.left_arrow_key_rect.width+self.right_arrow_key_rect.width+20),60))

        self.use_key_rect = self.use_key_text.get_rect()
        self.use_key_rect.topleft = (350+self.space_key_rect.width+self.space_key_text_rect.width+self.left_arrow_key_rect.width+10, 0)

       



    def startGame(self):
        FONT_COLOR=(0,0,0)
        clock = pygame.time.Clock()
        counter, text = 6, 'Starting in...'
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        
        run = True
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT: 
                    counter -= 1
                    if counter > 0:
                        text = str(counter) 
                    else:
                        # self.create_level(self.current_level)
                        # pygame.display.update()
                        self.run_level_check=True
                        break


                if event.type == pygame.QUIT: 
                    run = False
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    self.create_overworld(self.current_level,self.max_level)
                    
                

            # self.display_surface.fill((255, 255, 255))
            background_image = pygame.image.load('./Mario/homeBackground.jpg').convert_alpha()
            background_image = pygame.transform.scale(background_image, (1280, 700))
            self.screen.blit(background_image, (0, 0))
            font = pygame.font.Font("Royal Kingdom.ttf", 55)
            
            name1 = font.render("Place your hand in front of the camera", True, FONT_COLOR)
            name1Rect = name1.get_rect()
            name1Rect.center = (screen_width // 2, screen_height // 2 - 135)
            self.screen.blit(name1, name1Rect)
            
            name2 = font.render("Or press Esc to go back to menu", True, FONT_COLOR)
            name2Rect = name2.get_rect()
            name2Rect.center = (screen_width // 2, screen_height // 2 - 90)
            self.screen.blit(name2, name2Rect)
            
            timer = font.render(text, True, FONT_COLOR)
            timerRect = timer.get_rect()
            timerRect.center = (screen_width // 2, screen_height // 2 - 10)
            self.screen.blit(timer, timerRect)

        

            



            pygame.display.flip()
            clock.tick(60)
            
        
        pygame.display.update()
    def create_level(self, current_level):
        # self.run_level_check =False
        # self.startGame()
        FONT_COLOR=(0,0,0)
        start_time = time.time()
        seconds =6
        self.counter=6
        self.coins =0
        self.current_health=100
        
        font = pygame.font.Font("Royal Kingdom.ttf", 55)
        clock = pygame.time.Clock()
        run = True
        while run:
            current_time= time.time()
            elapsed_time = current_time - start_time

            if elapsed_time <= seconds:
                self.screen.fill((255, 255, 255))
                self.counter-=1
                # intCounter = str(int(elapsed_time/1000)*(-1))
                print(elapsed_time)
                intCounter = str(int(seconds - elapsed_time))
                print(self.counter)
                print(intCounter)
                
                background_image = pygame.image.load('./Mario/homeBackground.jpg').convert_alpha()
                background_image = pygame.transform.scale(background_image, (1280, 700))
                self.screen.blit(background_image, (0, 0))

                name1 = font.render("Place your hand in front of the camera", True, FONT_COLOR)
                name1Rect = name1.get_rect()
                name1Rect.center = (screen_width // 2, screen_height // 2 - 135)
                self.screen.blit(name1, name1Rect)
                
                name2 = font.render("Or press Esc to go back to menu", True, FONT_COLOR)
                name2Rect = name2.get_rect()
                name2Rect.center = (screen_width // 2, screen_height // 2 - 90)
                self.screen.blit(name2, name2Rect)
                

                # print(str(self.counter))
                timer = font.render(intCounter, True, FONT_COLOR)
                timerRect = timer.get_rect()
                timerRect.center = (screen_width // 2, screen_height // 2 - 10)
                self.screen.blit(timer, timerRect)
                pygame.display.update()
                clock.tick(60)
                pass
            else:
                self.run_level_check= True
                run=False

                
        
        if self.run_level_check:
            self.level = Level(current_level,self.screen,self.create_overworld,self.change_coins, self.change_health,self.level_bg_music)
            self.status='level'
            self.overworld_bg_music.stop()
            self.level_bg_music.play(loops=-1)
        
    def create_overworld(self, current_level, new_max_level):

        self.screen.blit(self.back_icon,(0,0))

        # self.space_key_rect.topleft = (450,20)

        # self.left_arrow_key_rect.topleft = (700,20)
        # self.right_arrow_key_rect.topleft = (700+(self.left_arrow_key_rect.width+20),20)

        
        if int(new_max_level) > int(self.max_level):
            self.overworld = Overworld(current_level,new_max_level, self.screen, self.create_level,self.create_overworld)
            self.max_level = new_max_level
        else:
            self.overworld = Overworld(0,0, self.screen, self.create_level,self.create_overworld)

        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops=-1)

    def change_coins(self, amount, theme):
        self.theme=theme
        self.coins+=amount

    def change_health(self,amount):
        self.current_health+=amount

    def check_game_over(self):
        if self.current_health<=0:
            self.current_health=100
            self.coins=0
            self.max_level=0
            self.overworld = Overworld(0, self.max_level,self.screen, self.create_level)
            self.status = 'overworld'
   
    

    def run(self,event):
        if self.status=='overworld' :
            menu_mouse_pos = pygame.mouse.get_pos()
            # print("back")
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if  self.back_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()
                        menu.main()

            self.overworld.run()
            self.screen.blit(self.back_icon,(0,0))
            
            self.screen.blit(self.use_key_text,self.use_key_rect)
            self.screen.blit(self.space_key,self.space_key_rect)
            self.screen.blit(self.space_key_text,self.space_key_text_rect)
            self.screen.blit(self.left_arrow_key,self.left_arrow_key_rect)
            self.screen.blit(self.right_arrow_key,self.right_arrow_key_rect)
            self.screen.blit(self.arrow_key_text,self.arrow_key_text_rect)
        
    
        if self.status=='level':
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins,self.theme)
            self.check_game_over()
            







def main():
    #Setting up pygame
    pygame.init()
    # screen_width = 1280
    # screen_height = 700
    # level = Level(level_0,screen)

    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game =  Game(screen)


    while True:
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                pygame.quit()
                # sys.exit()
        screen.fill('grey')
        game.run(event)
        # level.run()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()