import os
import sys
import pygame

pygame.init()

# Set up the Pygame display surface
window_size = (1280, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("GameBox")

background_image = pygame.image.load('launcher.png').convert()
background_image = pygame.transform.scale(background_image, window_size)

# Define the button properties for each game
button_color = (98, 179, 113)
button_size = (210, 80)
button_x1 = 140
button_y1 = 450
button_x2 = 555
button_y2 = 450
button_x3 = 940
button_y3 = 450


# Store the game properties in a dictionary
game1 = {'button_rect': pygame.Rect(button_x1, button_y1, button_size[0], button_size[1]), 'file': 'Mario/menu.py'}
game2 = {'button_rect': pygame.Rect(button_x2, button_y2, button_size[0], button_size[1]), 'file': 'Flappy/flappyBird.py'}
game3 = {'button_rect': pygame.Rect(button_x3, button_y3, button_size[0], button_size[1]), 'file': 'DinoGame/dino.py'}
games = [game1, game2, game3]

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check if the left mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for game in games:
                if game['button_rect'].collidepoint(mouse_pos):
                    pygame.quit()
                    os.system('python ' + game['file'])
                    quit()
            if exit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit()
    # Draw the background and the images
    screen.blit(background_image, (0, 0))

    # Draw the buttons and the text for each game
    for game in games:
        border_width = 3
        border_rect = pygame.Rect(game['button_rect'].left - border_width, game['button_rect'].top - border_width,
                                game['button_rect'].width + 2 * border_width, game['button_rect'].height + 2 * border_width)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, border_radius=20 + border_width)
        pygame.draw.rect(screen, button_color, game['button_rect'], border_radius=20)
        font = pygame.font.Font("Royal Kingdom.ttf", 60)
        
        # Render text with black color and offset
        text_outline = font.render("Play", True, (0, 0, 0))
        text_rect_outline = text_outline.get_rect(center=game['button_rect'].center)
        text_rect_outline.move_ip(2, 2)
        screen.blit(text_outline, text_rect_outline)

        # Render text with white color
        text = font.render("Play", True, (255, 255, 255))
        text_rect = text.get_rect(center=game['button_rect'].center)
        screen.blit(text, text_rect)

    exit_button = pygame.Rect(button_x2, button_y2+150, button_size[0], button_size[1])
    border_rect = pygame.Rect(exit_button.left-3,exit_button.top-3,exit_button.width+2*border_width,exit_button.height+2*border_width)

    pygame.draw.rect(screen, (0, 0, 0), border_rect, border_radius=20 + border_width)
    pygame.draw.rect(screen, (255,0,0), exit_button, border_radius=20)
    font = pygame.font.Font("Royal Kingdom.ttf", 60)
    
    # Render text with black color and offset
    text_outline = font.render("Quit", True, (0, 0, 0))
    text_rect_outline = text_outline.get_rect(center=exit_button.center)
    text_rect_outline.move_ip(2, 2)
    screen.blit(text_outline, text_rect_outline)

    # Render text with white color
    text = font.render("Quit", True, (255, 255, 255))
    text_rect = text.get_rect(center=exit_button.center)
    screen.blit(text, text_rect)

    pygame.display.update()