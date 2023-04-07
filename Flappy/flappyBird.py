import pygame, sys, random
from pygame.locals import *
from hand_control import *
import os


WINDOWWIDTH = 1280
WINDOWHEIGHT = 700

BIRDWIDTH = 30
BIRDHEIGHT = 30
G = 0.3
SPEEDFLY = -4
BIRDIMG = pygame.image.load('Flappy/img/bird.png')

COLUMNWIDTH = 60
COLUMNHEIGHT = 500
BLANK = 300
DISTANCE = 400

COLUMNIMG = pygame.image.load('Flappy/img/column.png')
settings_black = pygame.image.load("Flappy/img/gearBlack.png")
settings_white = pygame.image.load("Flappy/img/gearWhite.png")
BACKGROUND = pygame.image.load('Flappy/img/background.png')

isPaused = False

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
video =None
detector = None



DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')

level_music = pygame.mixer.Sound("Flappy/audio/level_music.wav")

theme = 'light'

class Bird():
    def __init__(self):
        self.width = BIRDWIDTH
        self.height = BIRDHEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 0
        self.surface = BIRDIMG

        self.check=""

    def draw(self):
        DISPLAYSURF.blit(self.surface, (int(self.x), int(self.y)))
    
    def draw_main(self):
        surface_scaled = pygame.transform.scale(self.surface,(self.surface.get_width()*1.75, self.surface.get_height()*1.75))
        # screen_rect = DISPLAYSURF.get_rect()
        surface_rect = self.surface.get_rect()
        surface_rect.x = 590
        surface_rect.y = 110
        DISPLAYSURF.blit(surface_scaled, surface_rect)


    def update(self,video,detector):
        self.y += self.speed + 0.5*G
        self.speed += G
        self.check = get_label_hand("",video,detector)
        
        if self.check=="beak":
            self.speed = SPEEDFLY

class Columns():
    def __init__(self,level='easy'):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        COLUMNSPEED = 10 #can be sued to set difficulty
        if level=='easy':
            self.speed = COLUMNSPEED
        if level=='medium':
            self.speed = COLUMNSPEED+10
        if level=='hard':
            self.speed = COLUMNSPEED+15
        self.surface = COLUMNIMG
        self.level = level
        self.ls = []
        for i in range(3):
            x = WINDOWWIDTH + i*self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 20)
            self.ls.append([x, y])
        
    def draw(self):

        for i in range(3):
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))
    
    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        
        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
            self.ls.append([x, y])

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(bird, columns):
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.width, bird.height]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > WINDOWHEIGHT:
        return True
    return False

class Score():
    def __init__(self):
        self.score = 0
        self.addScore = True
    
    def draw(self):
        font = pygame.font.Font('Royal Kingdom.ttf', 40)
        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
    def update(self, bird, columns):
        collision = False
        for i in range(3):
            rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rectBird = [bird.x, bird.y, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True

def gameStart(bird=Bird(),columns=Columns(),score= Score()):
    bird.__init__()

    # font = pygame.font.Font('Royal Kingdom.ttf'.ttf', 60)
    # headingSuface = font.render('FLAPPY BIRD', True, (255, 0, 0))
    # headingSize = headingSuface.get_size()
    
    # font = pygame.font.Font('Royal Kingdom.ttf'.ttf', 20)
    # commentSuface = font.render('Click to start', True, (0, 0, 0))
    # commentSize = commentSuface.get_size()
    
    while True:
        

        bg = pygame.image.load("Flappy/flappyBackground.png")
        bg_scaled = pygame.transform.scale(bg,(bg.get_width()*2, bg.get_height()*2))
        DISPLAYSURF.blit(pygame.transform.scale(bg_scaled,(WINDOWWIDTH,WINDOWHEIGHT)), (0, 0))
        # zbg = pygame.transform.scale(bg,(WINDOWWIDTH,WINDOWHEIGHT))
        bird.draw_main()
        # DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        # DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
        button_font = pygame.font.Font('Royal Kingdom.ttf', 55)
        button_width = 350
        button_height = 80
        button_padding = 40
        button_x = (WINDOWWIDTH  - button_width) // 2
        button_y = WINDOWHEIGHT // 2 - button_height

        # New Game button
        game_button_text = button_font.render("New Game", True, (0, 0, 0))
        game_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, (240,250,26,255), game_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), game_button_rect, 2, border_radius=20)  # black border
        game_button_text_rect = game_button_text.get_rect(center=game_button_rect.center)
        DISPLAYSURF.blit(game_button_text, game_button_text_rect)

        # Help button
        button_y += button_height + button_padding
        help_button_text = button_font.render("Help", True, (0, 0, 0))
        help_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, (240,250,26,255), help_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), help_button_rect, 2, border_radius=20)  # black border
        help_button_text_rect = help_button_text.get_rect(center=help_button_rect.center)
        DISPLAYSURF.blit(help_button_text, help_button_text_rect)
        
        # Exit button
        button_y += button_height + button_padding
        exit_button_text = button_font.render("Exit", True, (0, 0, 0))
        exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, (240,250,26,255), exit_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        DISPLAYSURF.blit(exit_button_text, exit_button_text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            menu_mouse_pos = pygame.mouse.get_pos()
            
            if event.type==pygame.MOUSEBUTTONDOWN and game_button_rect.collidepoint(menu_mouse_pos):
                # pygame.quit()
                # sys.exit()
                # os.system('python ' + 'mario.py')
                level = selectDifficulty()
                video , detector = initializer()
                startGameTimer(bird,columns,score,level)
                # gamePlay(bird,columns,score,level, video, detector)
                # return
                # print("play")
            if event.type==pygame.MOUSEBUTTONDOWN and  help_button_rect.collidepoint(menu_mouse_pos):
                print("Help Button Clicked")
                showHelp(screen=DISPLAYSURF)
                # ret_val = "help_menu"

                
                # return ret_val
            if event.type==pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(menu_mouse_pos):
                print("Exit button clicked") #connection to gamebox
                pygame.quit()
                # xyz.stop()
                os.system('python launcher.py')
                quit()
        # if event.type == MOUSEBUTTONDOWN:
        #     return
                
        pygame.display.update()
        fpsClock.tick(FPS)



def startGameTimer(bird,columns,score,level):
            global video, detector
            clock = pygame.time.Clock()
            counter, text = 6, 'Starting in...'
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            FONT_COLOR = (0,0,0)
            
            
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT: 
                        counter -= 1
                        if counter > 0 :
                            text = str(counter)
                        else:
                            video,detector = initializer()
                            gamePlay(bird,columns,score,level,video,detector)
                    if event.type == pygame.QUIT: 
                        run = False
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                        # menu(death_count=0)
                        gameStart()
                        pass
                    

                # DISPLAYSURF.fill((255, 255, 255))
                # background_image = BACKGROUND
                # background_image = pygame.transform.scale(background_image, (1280, 700))
                BACKGROUND_SCALED = pygame.transform.scale( BACKGROUND,(WINDOWWIDTH,WINDOWHEIGHT))
                DISPLAYSURF.blit(BACKGROUND_SCALED, (0, 0))
                font = pygame.font.Font("Royal Kingdom.ttf", 55)
                
                name1 = font.render("Place your hand in front of the camera", True, FONT_COLOR)
                name1Rect = name1.get_rect()
                name1Rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 135)
                DISPLAYSURF.blit(name1, name1Rect)
                
                name2 = font.render("Or press Esc to go back to menu", True, FONT_COLOR)
                name2Rect = name2.get_rect()
                name2Rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 75)
                DISPLAYSURF.blit(name2, name2Rect)
                
                timer = font.render(text, True, FONT_COLOR)
                timerRect = timer.get_rect()
                timerRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 10)
                DISPLAYSURF.blit(timer, timerRect)
                pygame.display.flip()
                clock.tick(60)
                
            
            pygame.display.update()


def gamePlay(bird, columns, score,level,video,detector):
    
    global isPaused, theme, level_music
    
    if bird is None and columns is None and score is None:
        bird.__init__()
        bird.speed = SPEEDFLY
        columns.__init__(level)
        score.__init__()
    else:
        level_music.play(loops=-1)
        beak_gesture = pygame.image.load("Flappy/img/beak_image.png").convert_alpha()
        beak_gesture_rect = beak_gesture.get_rect()
        beak_gesture_rect.topright = (50, 10)

        font_text = pygame.font.Font('Royal Kingdom.ttf',25)
        gesture_text = font_text.render("Bird Flies",True, (0,0,0))
        gesture_text_rect = gesture_text.get_rect()
        gesture_text_rect.topleft =( 50,beak_gesture_rect.y+15)

        screen_rect = DISPLAYSURF.get_rect()
        isPaused = False

        if theme=='light':
            BACKGROUND_SCALED = pygame.transform.scale( BACKGROUND,(WINDOWWIDTH,WINDOWHEIGHT))
            settings_scaled = pygame.transform.scale(settings_black, (50,50))
            settings_rect = settings_scaled.get_rect()
            settings_rect.topright =  (screen_rect.right - 10, screen_rect.top+10)
        if theme=='dark':
            back_black_bg = pygame.image.load("Flappy/flappyDarkBG.png")
            BACKGROUND_SCALED = pygame.transform.scale(back_black_bg,(WINDOWWIDTH,WINDOWHEIGHT))
            settings_scaled = pygame.transform.scale(settings_white, (50,50))
            settings_rect = settings_scaled.get_rect()
            settings_rect.topright =  (screen_rect.right - 10, screen_rect.top+10)
            
        while True:
            # mouseClick = False
            mouse_pos= pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == MOUSEBUTTONDOWN:
                #     mouseClick = True
                if event.type==MOUSEBUTTONDOWN:
                    if settings_rect.collidepoint(mouse_pos):
                        print("Settings button clicked")
                        
                        isPaused=True
                        while (isPaused):
                            # showSettings(isPaused)
                            executePause(bird,columns,score,level, video,detector)
                            
            
            
            
            DISPLAYSURF.blit(BACKGROUND_SCALED, (0, 0))
            
            # settings_black_rect.x = WINDOWWIDTH - (settings_black.get_width())
            # settings_black_rect.y = 10
            
            columns.draw()
            columns.update()
            bird.draw()
            bird.update(video,detector)
            score.draw()
            score.update(bird, columns)
            DISPLAYSURF.blit(settings_scaled,settings_rect)
            DISPLAYSURF.blit(beak_gesture, beak_gesture_rect)
            DISPLAYSURF.blit(gesture_text, gesture_text_rect)

            if isGameOver(bird, columns) == True:
                kill_feed(video)
                gameOver(bird,columns,score)

            pygame.display.update()
            fpsClock.tick(FPS)

def executePause(bird,columns,score,level, video, detector):
    themesRect,helpRect,exitRect,closeRect = showSettings()
    checkSettingsInput(themesRect,helpRect,exitRect,closeRect,bird,columns,score,level, video,detector)
    return

def gameOver(bird, columns, score):
    global theme
    level_music.stop()
    font = pygame.font.Font('Royal Kingdom.ttf', 60)
    headingSuface = font.render('GAME OVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    if theme=='light':
            BACKGROUND_SCALED = pygame.transform.scale( BACKGROUND,(WINDOWWIDTH,WINDOWHEIGHT))
    if theme=='dark':
        bg_black = pygame.image.load("Flappy/flappyDarkBG.png")
        BACKGROUND_SCALED = pygame.transform.scale(bg_black,(WINDOWWIDTH,WINDOWHEIGHT))
    DISPLAYSURF.blit(BACKGROUND_SCALED, (0, 0))
    
    font = pygame.font.Font('Royal Kingdom.ttf', 30)
    scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
    scoreSize = scoreSuface.get_size()

    columns.draw()
    bird.draw()
    DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
    DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))


    button_font = pygame.font.Font('Royal Kingdom.ttf', 55)
    button_width = 350
    button_height = 80
    button_padding = 40
    button_x = (WINDOWWIDTH  - button_width) // 2
    button_y = WINDOWHEIGHT // 2 - button_height

    game_button_text = button_font.render("Play Again", True, (0, 0, 0))
    game_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, (240,250,26,255), game_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), game_button_rect, 2, border_radius=20)  # black border
    game_button_text_rect = game_button_text.get_rect(center=game_button_rect.center)
    DISPLAYSURF.blit(game_button_text, game_button_text_rect)


    button_y += button_height + button_padding
    exit_button_text = button_font.render("Exit", True, (0, 0, 0))
    exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, (240,250,26,255), exit_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
    exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
    DISPLAYSURF.blit(exit_button_text, exit_button_text_rect)   

    
    # font = pygame.font.Font('Royal Kingdom.ttf'.ttf', 20)
    # commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    # commentSize = commentSuface.get_size()

    # font = pygame.font.Font('Royal Kingdom.ttf', 30)
    # scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
    # scoreSize = scoreSuface.get_size()

    
    

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            menu_mouse_pos = pygame.mouse.get_pos()
            
            if event.type==pygame.MOUSEBUTTONDOWN and game_button_rect.collidepoint(menu_mouse_pos):
                level = selectDifficulty()
                print(level)
                bird = Bird()
                columns = Columns(level)
                score_new = Score()
                # xyz = threadVideo()
                # xyz.start()
                video, detector = initializer()
                gamePlay(bird,columns,score_new,level,video,detector)
                kill_feed(video)
                gameOver(bird,columns,score_new)
                # return
            if event.type==pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(menu_mouse_pos):
                bird=Bird()
                gameStart(bird,columns,score)

            

        # if theme=='light':
        #     BACKGROUND_SCALED = pygame.transform.scale( BACKGROUND,(WINDOWWIDTH,WINDOWHEIGHT))
        # if theme=='dark':
        #     bg_black = pygame.image.load("Flappy/flappyDarkBG.png")
        #     BACKGROUND_SCALED = pygame.transform.scale(bg_black,(WINDOWWIDTH,WINDOWHEIGHT))
        # DISPLAYSURF.blit(BACKGROUND_SCALED, (0, 0))
        

        # columns.draw()
        # bird.draw()
        # DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        # DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))
        # DISPLAYSURF.blit(game_button_text, game_button_text_rect)
        # DISPLAYSURF.blit(exit_button_text, exit_button_text_rect)   
          

        pygame.display.update()
        fpsClock.tick(FPS)

def selectDifficulty(bird=Bird(), columns=Columns(), score =Score()):
    '''This is for selecting difficulty will change the column speed '''
    font = pygame.font.Font('Royal Kingdom.ttf', 60)
    headingSuface = font.render('SELECT DIFFICULTY', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    button_font = pygame.font.Font('Royal Kingdom.ttf',50)
    button_width = 200
    button_height = 100
    button_padding = 40
    button_x = (WINDOWWIDTH-button_width)//2
    button_y = (WINDOWHEIGHT//2) - button_height
    BACKGROUND_SCALED = pygame.transform.scale( BACKGROUND,(WINDOWWIDTH,WINDOWHEIGHT))
    DISPLAYSURF.blit(BACKGROUND_SCALED,(0,0))
    DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))

    #Easy button
    easy_button_text = button_font.render("Easy",True, (0,0,0))
    easy_button_rect = pygame.Rect(button_x,button_y,button_width,button_height)
    pygame.draw.rect(DISPLAYSURF,(240,250,26,255), easy_button_rect,border_radius=20)
    pygame.draw.rect(DISPLAYSURF,(0,0,0,0), easy_button_rect,2,border_radius=20)
    easy_button_text_rect = easy_button_text.get_rect(center = easy_button_rect.center)
    DISPLAYSURF.blit(easy_button_text,easy_button_text_rect)
    
    button_y += button_height + button_padding
    medium_button_text = button_font.render("Medium",True, (0,0,0))
    medium_button_rect = pygame.Rect(button_x,button_y,button_width,button_height)
    pygame.draw.rect(DISPLAYSURF,(240,250,26,255), medium_button_rect,border_radius=20)
    pygame.draw.rect(DISPLAYSURF,(0,0,0,0), medium_button_rect,2,border_radius=20)
    medium_button_text_rect = medium_button_text.get_rect(center = medium_button_rect.center)
    DISPLAYSURF.blit(medium_button_text,medium_button_text_rect)
    
    button_y += button_height + button_padding
    hard_button_text = button_font.render("Hard",True, (0,0,0))
    hard_button_rect = pygame.Rect(button_x,button_y,button_width,button_height)
    pygame.draw.rect(DISPLAYSURF,(240,250,26,255), hard_button_rect,border_radius=20)
    pygame.draw.rect(DISPLAYSURF,(0,0,0,0), hard_button_rect,2,border_radius=20)
    hard_button_text_rect = hard_button_text.get_rect(center = hard_button_rect.center)
    DISPLAYSURF.blit(hard_button_text,hard_button_text_rect)



    back_logo  =pygame.image.load("Flappy/backLogo.png")
    back_log_rect = back_logo.get_rect(topleft=(20,10))
    DISPLAYSURF.blit(back_logo,back_log_rect) 

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            
            # if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
            #     return

            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if easy_button_rect.collidepoint(mouse_pos):
                    print("Easy Button Clicked")
                    return_label = 'easy'
                    return return_label
                if medium_button_rect.collidepoint(mouse_pos):
                    print("Normal Button Clicked")
                    return_label = 'medium'
                    return return_label
                    return
                if hard_button_rect.collidepoint(mouse_pos):
                    print("hard Button Clicked")
                    return_label = 'hard'
                    return return_label
                    return
                if event.type==pygame.MOUSEBUTTONDOWN and back_log_rect.collidepoint(mouse_pos):
                    gameStart(bird,columns,score)
                    
        pygame.display.update()



def showHelp(screen): #main screen help
    background_image = pygame.image.load('Flappy/flappyBackground.png').convert()
    background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))
    background_image_rect = background_image.get_rect()
    background_image_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    screen.blit(background_image, background_image_rect)
    
    # draw buttons
    menu_text = pygame.font.Font('Royal Kingdom.ttf', 55)
    menu_text_back = pygame.font.Font('Royal Kingdom.ttf', 40)
    button_width = 425
    button_height = 80
    button_padding = 40
    button_x = (WINDOWWIDTH - button_width) // 2 - 325
    button_y = WINDOWHEIGHT // 2 - button_height

    # About Game button
    about_game_button_text = menu_text.render("About Game", True, (255,255, 255))
    about_game_button_rect = pygame.Rect(button_x, button_y - 70, button_width, button_height)
    pygame.draw.rect(screen, (1,27,205,255), about_game_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), about_game_button_rect, 2, border_radius=20)  # black border
    about_game_button_text_rect = about_game_button_text.get_rect(center=about_game_button_rect.center)
    screen.blit(about_game_button_text, about_game_button_text_rect)

    # How to play button
    button_y += button_height + button_padding
    htp_button_text = menu_text.render("How To Play", True, (0, 0, 0))
    htp_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (255, 255, 255, 255), htp_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), htp_button_rect, 2, border_radius=20)  # black border
    htp_button_text_rect = htp_button_text.get_rect(center=htp_button_rect.center)
    screen.blit(htp_button_text, htp_button_text_rect)

    # Back button
    back_button_text = menu_text_back.render("BACK", True, (255, 255, 255))
    back_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 - button_height + 350, 180, 60)
    pygame.draw.rect(screen, (1,27, 205, 255), back_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    screen.blit(back_button_text, back_button_text_rect)
    
    # #text box
    text_box_image = pygame.image.load("Flappy/settings.png")
    size = (650, 550)
    text_box_image = pygame.transform.scale(text_box_image, size)
    text_box_image_rect = text_box_image.get_rect()
    text_box_image_rect.center = (WINDOWWIDTH // 2 + 250, WINDOWHEIGHT // 2 - 50)
    
    # Create a font object
    text_font = pygame.font.Font('Royal Kingdom.ttf', 27)

    # Define the text to be rendered
    text_lines = [
        'Flappy Bird is a mobile game',
        'developed by Vietnamese developer', 'Dong Nguyen.',
        'The game features a simple,',
        'one-button game play where',
        'players control a bird by',
        'tapping the screen to',
        'make it flap its wings',
        'and navigate through a series of',
        'pipes without colliding with them.',
        'The game\'s difficulty lies in the',
        'precision required to successfully',
        'maneuver through the pipes,',
        'making it addictive and challenging.'
    ]

    # Render the text onto a surface
    text_surfaces = []
    max_line_width = 0  # Track the maximum line width
    for line in text_lines:
        text_surface = text_font.render(line, True, (0, 0, 0))
        text_surfaces.append(text_surface)
        line_width, line_height = text_font.size(line)
        max_line_width = max(max_line_width, line_width)

    # Calculate the height of the text box
    line_height = text_font.get_linesize()
    text_box_height = line_height * len(text_lines)

    # Create a new surface for the text box
    text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

    # Set the colorkey of the text box surface to be transparent
    text_box_surface.set_colorkey((255, 255, 255, 255))

    # Blit the text surfaces onto the text box surface
    for i, surface in enumerate(text_surfaces):
        text_box_surface.blit(surface, (0, i*line_height))

    # Blit the text box surface onto the screen
    screen.blit(text_box_image, text_box_image_rect)
    screen.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 65))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if about_game_button_rect.collidepoint(mouse_pos):
                    print('about game')
                elif htp_button_rect.collidepoint(mouse_pos):
                    print('Htp button clicked')
                    howToPlay(screen=screen)
                    pygame.display.update()
                    return
                elif back_button_text_rect.collidepoint(mouse_pos):
                    main()
                    return                  
        
        pygame.display.update()


def showSettings():
    
    
    flappySettings = pygame.image.load("Flappy/settingsFLappy.png")
    size = (500,500)
    flappySettings = pygame.transform.scale(flappySettings,size=size)

    screen_rect = DISPLAYSURF.get_rect()
    flappySettings_rect = flappySettings.get_rect()
    flappySettings_rect.center = screen_rect.center
    DISPLAYSURF.blit(flappySettings,flappySettings_rect)

    button_font = pygame.font.Font('Royal Kingdom.ttf', 55)
    button_width = 270
    button_height = 80
    button_padding = 40
    button_x = (WINDOWWIDTH - button_width) // 2 + 10
    button_y = flappySettings_rect.top + button_padding + 50
    FONT_COLOR = (0,0,0)

    #themes button
    themes_button_text = button_font.render("Themes", True, FONT_COLOR)
    themes_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), themes_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), themes_button_rect, 2, border_radius=20)  # black border
    themes_button_text_rect = themes_button_text.get_rect(center=themes_button_rect.center)
    DISPLAYSURF.blit(themes_button_text, themes_button_text_rect)

    # Help button
    button_y += button_height + button_padding
    help_button_text = button_font.render("Help", True, FONT_COLOR)
    help_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), help_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), help_button_rect, 2, border_radius=20)  # black border
    help_button_text_rect = help_button_text.get_rect(center=help_button_rect.center)
    DISPLAYSURF.blit(help_button_text, help_button_text_rect)

    # Exit button
    button_y += button_height + button_padding
    exit_button_text = button_font.render("Exit", True, FONT_COLOR)
    exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), exit_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
    exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
    DISPLAYSURF.blit(exit_button_text, exit_button_text_rect)

    close_button_rect = pygame.Rect(flappySettings_rect.left + 50, flappySettings_rect.top + 50, 50, 55)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), close_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
    close_text = button_font.render("X", True, (255, 255, 255))
    close_text_rect = close_text.get_rect(center=close_button_rect.center)
    DISPLAYSURF.blit(close_text, close_text_rect)
    pygame.display.update()

    return themes_button_rect,help_button_rect, exit_button_rect,close_button_rect

        

   
    
def checkSettingsInput(themesRect, helpRect, exitRect,closeRect,bird,columns,score,level, video,detector):
    global isPaused
    mouse_pos= pygame.mouse.get_pos()
        
    for event in pygame.event.get():
        if  event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            print("outside if ")
           
            isPaused= False
            
                # break
        
        if event.type == pygame.MOUSEBUTTONDOWN and isPaused:
                    # mouse_pos = pygame.mouse.get_pos()
            if themesRect.collidepoint(mouse_pos):
                print("Themes button clicked!")

                showThemes(bird,columns,score,level, video,detector)
                return
            elif helpRect.collidepoint(mouse_pos):
                print("Help button clicked!")
                htpInGame()
                return
            elif closeRect.collidepoint(mouse_pos):
                print("presseed close")
                isPaused=False
                pausedYes=False
                break
                return
                # unpause()
            elif exitRect.collidepoint(mouse_pos):
                print("presseed exit")
                kill_feed(video)
                exitGame()
                
                isPaused=False
                # pausedYes=False

                # os.system('python ' + 'menu.py')
                # menu.main()
                        # menu(death_count=0)
                        # pygame.display.flip()

def showThemes(bird,columns,score,level, video,detector):
    global light, dark, isPaused, theme
    
    themes_image = pygame.image.load("Flappy/settingsFLappy.png")
    size = (500, 500)
    themes_image = pygame.transform.scale(themes_image, size)
    themes_rect = themes_image.get_rect()
    themes_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(themes_image, themes_rect)
    
    # draw buttons
    button_font = pygame.font.Font('Royal Kingdom.ttf', 55)
    button_width = 180
    button_height = 180
    button_padding = 40
    button_x = (WINDOWWIDTH - button_width) // 2 + 10
    button_y = themes_rect.top + button_padding + 200
    
    # Light themes button
    light_image = pygame.image.load("Flappy/light.png")
    light_image = pygame.transform.scale(light_image, (button_width, button_height))
    light_button_rect = light_image.get_rect()
    light_button_rect.center = (button_x - 20, button_y - 20)
    DISPLAYSURF.blit(light_image, light_button_rect)
    
    # 'LIGHT' text
    light_text_surface = button_font.render('LIGHT', True, (255, 255, 255))
    light_text_rect = light_text_surface.get_rect()
    light_text_rect.midtop = (light_button_rect.centerx, light_button_rect.bottom + 5)
    DISPLAYSURF.blit(light_text_surface, light_text_rect)
    
    # Dark themes button
    dark_image = pygame.image.load("Flappy/dark.png")
    dark_image = pygame.transform.scale(dark_image, (button_width, button_height))
    dark_button_rect = dark_image.get_rect()
    dark_button_rect.center = (button_x + 190, button_y - 20)
    DISPLAYSURF.blit(dark_image, dark_button_rect)
    
    # 'DARK' text
    dark_text_surface = button_font.render('DARK', True, (0, 0, 0))
    dark_text_rect = dark_text_surface.get_rect()
    dark_text_rect.midtop = (dark_button_rect.centerx, dark_button_rect.bottom + 5)
    DISPLAYSURF.blit(dark_text_surface, dark_text_rect)
    
    # Back button
    back_button_text = button_font.render("BACK", True, (0, 0, 0))
    back_button_rect = pygame.Rect(button_x, button_y + 180, button_width, 60)
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), back_button_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    DISPLAYSURF.blit(back_button_text, back_button_text_rect)
    
    # # Close button
    # close_button_rect = pygame.Rect(themes_rect.left + 50, themes_rect.top + 50, 50, 55)
    # pygame.draw.rect(DISPLAYSURF, (0, 0, 0), close_button_rect, border_radius=20)
    # pygame.draw.rect(DISPLAYSURF, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
    # close_text = button_font.render("X", True, (255, 255, 255))
    # close_text_rect = close_text.get_rect(center=close_button_rect.center)
    # DISPLAYSURF.blit(close_text, close_text_rect)
    
    while isPaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                # unpause()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if light_button_rect.collidepoint(mouse_pos):
                    print("Light themes button clicked!")
                    theme='light'

                    gamePlay(bird,columns,score,level, video,detector)
                    isPaused = False
                    
                    
                    
                   
                    pygame.display.update()
                    return
                elif dark_button_rect.collidepoint(mouse_pos):
                    print("Dark themes button clicked!")
                    theme='dark'
                    isPaused = False
                    gamePlay(bird,columns,score,level, video,detector)
                    # gamePlay()
                    
                    pygame.display.update()
                    return
                elif back_button_rect.collidepoint(mouse_pos):
                    print("Back button clicked")
                    # paused()
                    isPaused=False
                    pygame.display.flip()
                    return
                # elif close_button_rect.collidepoint(mouse_pos):
                #     # unpause()
                #     return
        
        pygame.display.flip()

    
def htpInGame():
        global isPaused
        #text box
        text_box_image = pygame.image.load("Flappy/settingsFLappy.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        
        # Create a font object
        text_font = pygame.font.Font('Royal Kingdom.ttf', 24)

        # Define the text to be rendered
        text_lines = [
            'The original version of the','game had keyboard or touch','as the mode of input ','Our redesign focuses on','increasing this game\'s','accessibility. ',
            'For playing the game with','hand gestures -','To control the movement of','Flappy Bird ->',
            'Join the THUMB and INDEX FINGER'
            ]

        # Render the text onto a surface
        text_surfaces = []
        max_line_width = 0  # Track the maximum line width
        for line in text_lines:
            text_surface = text_font.render(line, True, (0, 0, 0))
            text_surfaces.append(text_surface)
            line_width, line_height = text_font.size(line)
            max_line_width = max(max_line_width, line_width)

        # Calculate the height of the text box
        line_height = text_font.get_linesize()
        text_box_height = line_height * len(text_lines)

        # Create a new surface for the text box
        text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

        # Set the colorkey of the text box surface to be transparent
        text_box_surface.set_colorkey((255, 255, 255, 255))

        # Blit the text surfaces onto the text box surface
        for i, surface in enumerate(text_surfaces):
            text_box_surface.blit(surface, (0, i*line_height))

        # Blit the text box surface onto the screen
        DISPLAYSURF.blit(text_box_image, text_box_image_rect)
        DISPLAYSURF.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 65))
        
        # draw buttons
        button_font = pygame.font.Font('Royal Kingdom.ttf', 30)
        button_width = 180
        button_height = 180
        button_padding = 40
        button_x = (WINDOWWIDTH - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Back button
        back_button_text = button_font.render("BACK", True, (0, 0, 0))
        back_button_rect = pygame.Rect(button_x, button_y + 200, button_width, 35)
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        DISPLAYSURF.blit(back_button_text, back_button_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    # unpause()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        print("Back button clicked")
                        isPaused = False
                        # paused()
                        pygame.display.update()
                        return
        
            pygame.display.update()



def howToPlay(screen):
    background_image = pygame.image.load('Flappy/flappyBackground.png').convert_alpha()
    background_image = pygame.transform.scale(background_image, (1280, 700))
    background_image_rect = background_image.get_rect()
    background_image_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    screen.blit(background_image, background_image_rect)
    
    # draw buttons
    menu_text = pygame.font.Font('Royal Kingdom.ttf', 55)
    menu_text_back = pygame.font.Font('Royal Kingdom.ttf', 40)
    button_width = 425
    button_height = 80
    button_padding = 40
    button_x = (WINDOWWIDTH - button_width) // 2 - 325
    button_y = WINDOWHEIGHT // 2 - button_height

    # About Game button
    about_game_button_text = menu_text.render("About Game", True, (0, 0, 0))
    about_game_button_rect = pygame.Rect(button_x, button_y - 70, button_width, button_height)
    pygame.draw.rect(screen, (255, 255, 255, 255), about_game_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), about_game_button_rect, 2, border_radius=20)  # black border
    about_game_button_text_rect = about_game_button_text.get_rect(center=about_game_button_rect.center)
    screen.blit(about_game_button_text, about_game_button_text_rect)

    # How to play button
    button_y += button_height + button_padding
    htp_button_text = menu_text.render("How To Play", True, (255, 255, 255))
    htp_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (1,27,205,255), htp_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), htp_button_rect, 2, border_radius=20)  # black border
    htp_button_text_rect = htp_button_text.get_rect(center=htp_button_rect.center)
    screen.blit(htp_button_text, htp_button_text_rect)

    # Back button
    back_button_text = menu_text_back.render("BACK", True, (255, 255, 255))
    back_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 - button_height + 350, 180, 60)
    pygame.draw.rect(screen, (1,27, 205, 255), back_button_rect, border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    screen.blit(back_button_text, back_button_text_rect)
    
    #text box
    text_box_image = pygame.image.load("Flappy/settings.png")
    size = (650, 550)
    text_box_image = pygame.transform.scale(text_box_image, size)
    text_box_image_rect = text_box_image.get_rect()
    text_box_image_rect.center = (WINDOWWIDTH // 2 + 250, WINDOWHEIGHT // 2 - 50)
    
    # Create a font object
    text_font = pygame.font.Font('Royal Kingdom.ttf', 30)

    # Define the text to be rendered
    text_lines = [
            'The original version of the','game had keyboard or touch','as the mode of input ','Our redesign focuses on','increasing this game\'s','accessibility. ',
            'For playing the game with','hand gestures -','To control the movement of','Flappy Bird ->',
            'Join the THUMB and INDEX FINGER'
            ]

    # Render the text onto a surface
    text_surfaces = []
    max_line_width = 0  # Track the maximum line width
    for line in text_lines:
        text_surface = text_font.render(line, True, (0, 0, 0))
        text_surfaces.append(text_surface)
        line_width, line_height = text_font.size(line)
        max_line_width = max(max_line_width, line_width)

    # Calculate the height of the text box
    line_height = text_font.get_linesize()
    text_box_height = line_height * len(text_lines)

    # Create a new surface for the text box
    text_box_surface = pygame.Surface((max_line_width, text_box_height), pygame.SRCALPHA)  # Set the alpha channel

    # Set the colorkey of the text box surface to be transparent
    text_box_surface.set_colorkey((255, 255, 255, 255))

    # Blit the text surfaces onto the text box surface
    for i, surface in enumerate(text_surfaces):
        text_box_surface.blit(surface, (0, i*line_height))

    # Blit the text box surface onto the screen
    screen.blit(text_box_image, text_box_image_rect)
    screen.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 65))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if about_game_button_rect.collidepoint(mouse_pos):
                    print('about game')
                    showHelp(screen=screen)
                    pygame.display.update()
                    return
                elif htp_button_rect.collidepoint(mouse_pos):
                    print('Htp button clicked')
                    # howToPlay()
                elif back_button_text_rect.collidepoint(mouse_pos):
                    main()
                    return                  
        
        pygame.display.update()


def exitGame():
        global isPaused
        #text box
        FONT_COLOR = (0,0,0)
        text_box_image = pygame.image.load("Flappy/settingsFlappy.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        
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
        DISPLAYSURF.blit(text_box_image, text_box_image_rect)
        DISPLAYSURF.blit(text_box_surface, (text_box_image_rect.left + 55, text_box_image_rect.top + 90))
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 180
        button_height = 120
        button_padding = 40
        button_x = (WINDOWWIDTH - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Yes button
        yes_button_text = button_font.render("YES", True, FONT_COLOR)
        yes_button_rect = pygame.Rect(button_x - 115, button_y, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), yes_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), yes_button_rect, 2, border_radius=20)  # black border
        yes_button_text_rect = yes_button_text.get_rect(center=yes_button_rect.center)
        DISPLAYSURF.blit(yes_button_text, yes_button_text_rect)
        
        # No button
        no_button_text = button_font.render("NO", True, FONT_COLOR)
        no_button_rect = pygame.Rect(button_x + 105, button_y, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), no_button_rect, border_radius=20)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), no_button_rect, 2, border_radius=20)  # black border
        no_button_text_rect = no_button_text.get_rect(center=no_button_rect.center)
        DISPLAYSURF.blit(no_button_text, no_button_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    # unpause()

                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button_rect.collidepoint(mouse_pos):
                        # menu(death_count=0)
                        pygame.quit()
                        os.system('python launcher.py')
                        quit() 
                        return
                    elif no_button_rect.collidepoint(mouse_pos):
                        # paused()
                        pygame.display.update()
                        return
        
            pygame.display.update()



def main():
    bird = Bird()
    columns = Columns()
    score = Score()
    
    
    while True:
        
        gameStart(bird,columns,score)
        # level = selectDifficulty()
        
        # gamePlay(bird, columns, score, xyz,level)
        # gameOver(bird, columns, score)

if __name__ == '__main__':
    main()