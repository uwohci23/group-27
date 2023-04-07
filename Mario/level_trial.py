import pygame
from settings import *
from level2 import levels

class LevelTry:
    def __init__(self, current_level,surface, create_overworld):
        
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[self.current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        #level display
        self.font = pygame.font.Font(None,40)
        self.text_surface = self.font.render(level_content, True, 'White')
        self.text_rect = self.text_surface.get_rect(center = (screen_width/2, screen_height/2))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            print(type(self.new_max_level))
            self.new_max_level = int(self.new_max_level)
            self.create_overworld(self.current_level, self.new_max_level)
           
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)
            
    def run(self):
        self.input()
        self.display_surface.blit(self.text_surface,self.text_rect)
