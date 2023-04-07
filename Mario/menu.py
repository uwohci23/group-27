import pygame,sys
from button import Button
import os
from settings import *
import mario


def main():
    pygame.init()
    pygame.mixer.music.stop()
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Menu")
    green = (0, 255, 0)
    blue = (0, 0, 128)

    tilte_image = pygame.image.load('./Mario/graphics/superMarioFont.jpg').convert_alpha()
    tilte_image_rect = tilte_image.get_rect()
    tilte_image_rect.x = 420
    tilte_image_rect.y = 30
    bg = pygame.image.load("./Mario/homeBackground.jpg").convert_alpha()
    bg = pygame.transform.scale(bg, (1280, 700))
    # font = pygame.font.Font("Royal Kingdom.ttf",40)

    def get_font(size):
        return pygame.font.Font("Royal Kingdom.ttf",size)


        
    pygame.display.set_caption("Menu")
    while True:
        screen.blit(bg,(0,0))   
        screen.blit(tilte_image, tilte_image_rect)
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("Main Menu",True,green,blue)
        menu_rect = menu_text.get_rect(center = (640,100))


        # play_button = Button(image=pygame.image.load("assets/Play_Rect.png").convert_alpha(), pos=(640, 250), 
        #                     text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        # options_button = Button(image=pygame.image.load("assets/Options_Rect.png"), pos=(640, 400), 
        #                     text_input="HELP", font=get_font(75),base_color="#d7fcd4", hovering_color="White")

        # quit_button = Button(image=pygame.image.load("assets/Quit_Rect.png"), pos=(640, 550), 
        #                     text_input="QUIT", font=get_font(75),base_color="#d7fcd4", hovering_color="White")
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 350
        button_height = 80
        button_padding = 40
        button_x = (screen_width  - button_width) // 2
        button_y = screen_height // 2 - button_height

        # New Game button
        game_button_text = button_font.render("New Game", True, (255, 255, 255))
        game_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (1, 27, 205, 255), game_button_rect, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), game_button_rect, 2, border_radius=20)  # black border
        game_button_text_rect = game_button_text.get_rect(center=game_button_rect.center)
        screen.blit(game_button_text, game_button_text_rect)

        # Help button
        button_y += button_height + button_padding
        help_button_text = button_font.render("Help", True, (255, 255, 255))
        help_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (1,27,205,255), help_button_rect, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), help_button_rect, 2, border_radius=20)  # black border
        help_button_text_rect = help_button_text.get_rect(center=help_button_rect.center)
        screen.blit(help_button_text, help_button_text_rect)
        
        # Exit button
        button_y += button_height + button_padding
        exit_button_text = button_font.render("Exit", True, (255, 255, 255))
        exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (1,27,205,255), exit_button_rect, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_button_text, exit_button_text_rect)
        
        # screen.blit(button_font, menu_rect)

        for button in [game_button_rect,help_button_rect,exit_button_rect]:
            # button.changeColor(menu_mouse_pos)
            # button.update(screen=screen)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if game_button_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()
                        # sys.exit()
                        # os.system('python ' + 'mario.py')
                        mario.main()
                        # print("play")
                    if  help_button_rect.collidepoint(menu_mouse_pos):
                        showHelp(screen=screen)
                        # ret_val = "help_menu"

                        
                        # return ret_val
                    if exit_button_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()
                        os.system('python launcher.py')
                        quit()  

        pygame.display.flip()


def showHelp(screen): #main screen help
            background_image = pygame.image.load('./Mario/homeBackground.jpg').convert()
            background_image = pygame.transform.scale(background_image, (1280, 700))
            background_image_rect = background_image.get_rect()
            background_image_rect.center = (screen_width // 2, screen_height // 2)
            screen.blit(background_image, background_image_rect)
            
            # draw buttons
            menu_text = pygame.font.Font("Royal Kingdom.ttf", 55)
            menu_text_back = pygame.font.Font("Royal Kingdom.ttf", 40)
            button_width = 425
            button_height = 80
            button_padding = 40
            button_x = (screen_width - button_width) // 2 - 325
            button_y = screen_height // 2 - button_height

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
            back_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - button_height + 350, 180, 60)
            pygame.draw.rect(screen, (1,27, 205, 255), back_button_rect, border_radius=20)
            pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
            back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
            screen.blit(back_button_text, back_button_text_rect)
            
            # #text box
            text_box_image = pygame.image.load("./Mario/graphics/settings.png")
            size = (650, 550)
            text_box_image = pygame.transform.scale(text_box_image, size)
            text_box_image_rect = text_box_image.get_rect()
            text_box_image_rect.center = (screen_width // 2 + 250, screen_height // 2 - 50)
            
            # Create a font object
            text_font = pygame.font.Font("Royal Kingdom.ttf", 40)

            # Define the text to be rendered
            text_lines = [
                'The Super Mario Bros is','a platform game developed and','published by Nintendo for the','Nindtendo Entertainment', 'System(NDS).','The successor to the 1983','arcade game Mario Bros and','the first game in the','Super Mario Series.'
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

def howToPlay(screen):
        background_image = pygame.image.load('./Mario/homeBackground.jpg').convert_alpha()
        background_image = pygame.transform.scale(background_image, (1280, 700))
        background_image_rect = background_image.get_rect()
        background_image_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(background_image, background_image_rect)
        
        # draw buttons
        menu_text = pygame.font.Font("Royal Kingdom.ttf", 55)
        menu_text_back = pygame.font.Font("Royal Kingdom.ttf", 40)
        button_width = 425
        button_height = 80
        button_padding = 40
        button_x = (screen_width - button_width) // 2 - 325
        button_y = screen_height // 2 - button_height

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
        back_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - button_height + 350, 180, 60)
        pygame.draw.rect(screen, (1,27, 205, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text, back_button_text_rect)
        
        #text box
        text_box_image = pygame.image.load("./Mario/graphics/settings.png")
        size = (650, 550)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (screen_width // 2 + 250, screen_height // 2 - 50)
        
        # Create a font object
        text_font = pygame.font.Font("Royal Kingdom.ttf", 30)

        # Define the text to be rendered
        text_lines = [
            'The original version of the game had ', 
            'keyboard as the mode of input. Our ',
            'redesign focuses on increasing this ',
            'game\'s accessibility. ',
            '',
            'For playing the game with hand gestures -',
            '1. Right hand thumb out -> Move Left',
            '2. Open palm (all 5 fingers up) -> Jump',
            '3. Left hand thumb out -> Move Right'
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
        
    # FONT_COLOR=(0,0,0)
    #     # screen.fill((255, 255, 255))
    # font = pygame.font.Font("Royal Kingdom.ttf", 40)
    # background_image = pygame.image.load('./Mario/homeBackground.png').convert()
    # background_image = pygame.transform.scale(background_image, (1280, 700))
    # screen.blit(background_image, (0, 0))
    
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         run = False
    #         pygame.display.quit()
    #         pygame.quit()
    #         exit()

if __name__ == "__main__":
    main()
# main_menu()
# pygame.display.update()