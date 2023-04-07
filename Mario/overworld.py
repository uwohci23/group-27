import pygame
from game_data import levels
from support import import_folder
from decoration import Sky
from settings import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frames_index =0
        self.image = self.frames[self.frames_index]

        if status=='unlocked':
            self.status = 'unlocked'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2),icon_speed,icon_speed)

    def animate(self):
        self.frames_index +=0.15
        if (self.frames_index>=len(self.frames)):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self):
        if self.status == 'unlocked':
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface,(0,0))
class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos  =pos
        self.image = pygame.image.load('./Mario/graphics/overworld/hat.png').convert_alpha()
        
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, create_overworld):

        #setup 
        self.display_surface = surface
        self.max_level  = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.create_overworld = create_overworld

        # $movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.moving=False

        #sprites
        self.sky = Sky(8,'light','overworld')
        
        #countdown
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 2000

        



        self.setup_nodes()
        self.setup_icon()

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate( levels.values()):
            if int(index)<=int(self.max_level):
                node_sprite = Node(node_data['node_pos'], 'unlocked', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'],'locked',self.speed, node_data['node_graphics'])

            self.nodes.add(node_sprite)

    def draw_paths(self):
        if int(self.max_level)>0:
            points =[node['node_pos'] for index, node in enumerate(levels.values())if int(index)<=int(self.max_level)]
            pygame.draw.lines(self.display_surface,'#a04f45', False, points, 6)

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
                            self.create_level(self.current_level)
                            # pygame.display.update()
                    if event.type == pygame.QUIT: 
                        run = False
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                        self.create_overworld(self.current_level,self.max_level)
                        
                    

                # self.display_surface.fill((255, 255, 255))
                background_image = pygame.image.load('./Mario/homeBackground.jpg').convert_alpha()
                background_image = pygame.transform.scale(background_image, (1280, 700))
                self.display_surface.blit(background_image, (0, 0))
                font = pygame.font.Font("Royal Kingdom.ttf", 55)
                
                name1 = font.render("Place your hand in front of the camera", True, FONT_COLOR)
                name1Rect = name1.get_rect()
                name1Rect.center = (screen_width // 2, screen_height // 2 - 135)
                self.display_surface.blit(name1, name1Rect)
                
                name2 = font.render("Or press Esc to go back to menu", True, FONT_COLOR)
                name2Rect = name2.get_rect()
                name2Rect.center = (screen_width // 2, screen_height // 2 - 90)
                self.display_surface.blit(name2, name2Rect)
                
                timer = font.render(text, True, FONT_COLOR)
                timerRect = timer.get_rect()
                timerRect.center = (screen_width // 2, screen_height // 2 - 10)
                self.display_surface.blit(timer, timerRect)
                pygame.display.flip()
                clock.tick(60)
                
            
            pygame.display.update()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and int(self.current_level) < int(self.max_level):
                self.move_direction = self.get_movement_data('next')
                self.current_level+=1
                self.moving = True

            if keys[pygame.K_LEFT] and self.current_level > 0:
                print("Previous")
                self.move_direction = self.get_movement_data('previous')
                self.current_level-=1
                self.moving = True

            if keys[pygame.K_SPACE]:
                # self.startGame()
                self.create_level(self.current_level)



    def update_icon_pos(self):
        if self.move_direction and self.moving:
            self.icon.sprite.pos+= self.move_direction*self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                print("collidezone")
                self.moving=False
                self.move_direction = pygame.math.Vector2(0,0)

        

    def get_movement_data(self, moveDir):
        
        start  = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        
        if moveDir=='next':
            print("inside next")
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
            print(end)
            
        elif moveDir=='previous':
            print("inside previous")
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)

        return (end-start).normalize()
    
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input =True

    
        
    def run(self):
        self.input_timer()
        self.input() 
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

