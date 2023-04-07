import pygame
from tile import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from player import Player
from settings import tile_size, screen_width, screen_height
from particles import Particle_Effect
from support import import_csv_layout, import_cut_graphics
from decoration import Sky, Water, Cloud
from game_data import levels
from hand_control import *
import os
import menu
#surface  - the display surface where everything will be displayed
#level_data is the level_map
class Level:
    def __init__(self,current_level,surface,create_overworld, change_coins, change_health,level_bg_music):

        self.video, self.detector = initializer()
        self.paused_game =False

        self.level_bg_music = level_bg_music
        #settting up the level
        self.display_surface = surface #setting the surface
        # self.setup_layout(level_data) #setting the map 
        self.world_shift =-3 #world shift
        self.current_x = 0 #wherre the collision has occured 

        #audio
        self.coin_sound = pygame.mixer.Sound('./Mario/audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('./Mario/audio/effects/stomp.wav')


        #dust
        self.dust_sprite  = pygame.sprite.GroupSingle()
    
        self.player_on_ground = False

        #explosion particles
        self.explosion_sprites = pygame.sprite.Group()



        self.current_level = current_level
        level_data = levels[self.current_level]
        # level_content = levels['content']
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # self.font = pygame.font.Font(None,40)
        # self.text_surface = self.font.render(level_content, True, 'White')
        # self.text_rect = self.text_surface.get_rect(center = (screen_width/2, screen_height/2))

        #player layout
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout,change_health) 
        
        #theme setting
        self.theme = 'light'

        #user interface 
        self.change_coins = change_coins

        #terrain_setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        #crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout,'crates')

        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coin_layout,'coins')

        #fg palm trees
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

        #bg palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')    

        #constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        #decoratopm
        self.sky =  Sky(horizon =8,theme=self.theme)
        level_width = len(terrain_layout[0])*tile_size
        self.water = Water(screen_height-40, level_width)
        self.cloud = Cloud(400, level_width, 30)
        self.settings_icon = pygame.image.load("./Mario/graphics/gearBlack.png")
        self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
        self.settings_rect = self.settings_icon.get_rect()
        self.settings_rect.topright = (screen_width - 50,15)

        #hand gestures images
        self.jump_gesture = pygame.image.load("Mario/graphics/gestures/openHand.png").convert_alpha()
        self.jump_gesture_rect = self.jump_gesture.get_rect()
        self.leftHandOut_gesture = pygame.image.load("Mario/graphics/gestures/leftHandThumb.png").convert_alpha()
        self.leftHandOut_gesture_rect = self.leftHandOut_gesture.get_rect()
        self.rightHandThumb_gesture = pygame.image.load("Mario/graphics/gestures/rightHandThumb.png").convert_alpha()
        self.rightHandThumb_gesture_rect  = self.rightHandThumb_gesture.get_rect() 


        # self.display_surface.blit(self.settings_icon, self.settings_rect)

        


    def setup_player(self, layout,change_health):
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row): 
                x=column_index*tile_size
                y=row_index*tile_size
                if column== '0': 
                    sprite = Player((x,y),self.display_surface,self.create_jump_run_particle,change_health,self.video,self.detector)
                    self.player.add(sprite)
                if column=='1':
                    hat_surface = pygame.image.load('./Mario/graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,surface=hat_surface)
                    self.goal.add(sprite)

    


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row): 
                if column!= '-1': #because we import string of  numbers
                    x=column_index*tile_size
                    y=row_index*tile_size

                    if(type=='terrain'):
                        terrain_tile_list = import_cut_graphics('./Mario/graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(column)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        

                    if(type=='grass'):
                        grass_tile_list = import_cut_graphics('./Mario/graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(column)]
                        sprite = StaticTile(tile_size, x,y,tile_surface)

                    if type=='crates':
                        sprite = Crate(tile_size,x,y)
                    
                    if type=='coins':
                        if column =='0':
                            sprite = Coin(tile_size,x,y,'./Mario/graphics/coins/gold',5)
                        else:
                            
                            sprite = Coin(tile_size,x,y,'./Mario/graphics/coins/silver',1)

                    if type=='fg palms':
                        if column == '0' : 
                            sprite = Palm(tile_size,x,y,'./Mario/graphics/terrain/palm_small',38)
                        if column =='1': 
                            sprite = Palm(tile_size,x,y,'./Mario/graphics/terrain/palm_large',64)
                    
                    if type=='bg palms': 
                        sprite = Palm(tile_size,x,y,'./Mario/graphics/terrain/palm_bg',64)

                    if type=='enemies':
                        sprite = Enemy(tile_size,x,y)
                    
                    if type=='constraint':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)
        return sprite_group



    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites,False):
                enemy.reverse()


    def check_enemy_collisions(self):
        enemy_collisions= pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if int(enemy_top) < int(player_bottom) <int(enemy_center) and int(self.player.sprite.direction.y)>=0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -8
                    explosion_sprite = Particle_Effect(enemy.rect.center ,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()
                    


    def create_jump_run_particle(self,pos):
        jump_particle_sprite = Particle_Effect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos+=pygame.math.Vector2(10,-5)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            # print(self.player.sprite.on_ground)
            self.player.on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if  self.player_on_ground ==False and self.player.sprite.on_ground == True and  self.dust_sprite.sprites()==None:
            print("inside condition ")
            
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = Particle_Effect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)
            # print(self.dust_sprite)

    # def setup_layout(self, layout):
    #     #printing the level on self.display_surface 
    #     self.tiles=pygame.sprite.Group()
    #     self.player =pygame.sprite.GroupSingle()
    #     for row_index, row in enumerate(layout) : #getting the row values
    #         for column_index, column in enumerate(row):
    #             #checking if X then adding it in the group of tiles to print on the self.display_surface
    #             x=column_index*tile_size #up - down
    #             y=row_index*tile_size #left right
    #             if column=='X':
    #                 tile =Tile(pos = (x,y),size=tile_size)
    #                 self.tiles.add(tile)
    #             if column=='P':
    #                 player_sprite = Player(pos = (x,y),surface = self.display_surface,create_jump_particles = self.create_jump_run_particle) #without the brackets because it is not a call
    #                 self.player.add(player_sprite)

    def check_death(self):
        
        if self.player.sprite.rect.top>screen_height :
            get_label_hand("kill_int",self.video,self.detector)
            kill_feed(self.video)
            self.create_overworld(self.current_level, 0)
        

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal,False) :
            get_label_hand("kill_int",self.video,self.detector)
            kill_feed(self.video)
            self.create_overworld(self.current_level, self.new_max_level)

    def horizointal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites()+self.crates_sprites.sprites()+self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x>0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.collision_rect.right
                elif player.direction.x<0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.collision_rect.left 
       


    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()+self.crates_sprites.sprites()+self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y<0: #going up
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y>0: #going down
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0 # setting the direction of movement to 0 as it should not go beyond the tile
                    player.on_ground = True
        if player.on_ground and player.direction.y<0 or player.direction.y>1:
            player.on_ground=False
        

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x<screen_width/4 and direction_x<0:
            # print(direction_x)
            self.world_shift=8
            player.speed = 0
        
        elif player_x>screen_width-(screen_width/4) and direction_x>0:
            # print(direction_x)
            self.world_shift = -8
            player.speed = 0

        else:
            self.world_shift=0
            player.speed =8
    
    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value, self.theme)

    
        


    def pauseGame(self):
        
            mouse_pos= pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if self.settings_rect.collidepoint(mouse_pos):
                        print("Open settings menu")
                        self.paused_game = True
                        self.paused()
                        
            
    
    def paused(self):
        self.settings_Dialog()
        while self.paused_game:
            self.check_input()



    

            
    

    def settings_Dialog(self):
        global button_font, help_button_rect, themes_button_rect, close_button_rect, exit_button_rect
        
                # print("Enterreed if")
        self.settings_bg = pygame.image.load("./Mario/graphics/settings.png").convert_alpha()
        size = (500, 500)
        self.settings_bg = pygame.transform.scale(self.settings_bg, size)
        self.settings_bg_rect = self.settings_bg.get_rect()
        self.settings_bg_rect.center = (screen_width // 2, screen_height // 2)
        self.display_surface.blit(self.settings_bg,self.settings_bg_rect)

        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 270
        button_height = 80
        button_padding = 40
        button_x = (screen_width - button_width) // 2 + 10
        button_y = self.settings_bg_rect.top + button_padding + 50
        FONT_COLOR = (0,0,0)

        #themes button
        themes_button_text = button_font.render("Themes", True, FONT_COLOR)
        themes_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.display_surface, (255, 255, 255), themes_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), themes_button_rect, 2, border_radius=20)  # black border
        themes_button_text_rect = themes_button_text.get_rect(center=themes_button_rect.center)
        self.display_surface.blit(themes_button_text, themes_button_text_rect)

        # Help button
        button_y += button_height + button_padding
        help_button_text = button_font.render("Help", True, FONT_COLOR)
        help_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.display_surface, (255, 255, 255), help_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), help_button_rect, 2, border_radius=20)  # black border
        help_button_text_rect = help_button_text.get_rect(center=help_button_rect.center)
        self.display_surface.blit(help_button_text, help_button_text_rect)

        # Exit button
        button_y += button_height + button_padding
        exit_button_text = button_font.render("Exit", True, FONT_COLOR)
        exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.display_surface, (255, 255, 255), exit_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), exit_button_rect, 2, border_radius=20)  # black border
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        self.display_surface.blit(exit_button_text, exit_button_text_rect)

        close_button_rect = pygame.Rect(self.settings_bg_rect.left + 50, self.settings_bg_rect.top + 50, 50, 55)
        pygame.draw.rect(self.display_surface, (0, 0, 0), close_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
        close_text = button_font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_button_rect.center)
        self.display_surface.blit(close_text, close_text_rect)
        
        pygame.display.flip()

    def check_input(self):
        mouse_pos= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if  event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                        print("outside if ")
                        self.paused_game = False
                            # break

            if event.type == pygame.MOUSEBUTTONDOWN and self.paused_game:
                        # mouse_pos = pygame.mouse.get_pos()
                if themes_button_rect.collidepoint(mouse_pos):
                    print("Themes button clicked!")
                    self.showThemes()
                elif help_button_rect.collidepoint(mouse_pos):
                    print("Help button clicked!")
                    self.htpInGame()
                elif close_button_rect.collidepoint(mouse_pos):
                    print("presseed close")
                    self.paused_game=False
                    # unpause()
                elif exit_button_rect.collidepoint(mouse_pos):
                    print("presseed exit")
                    self.exitGame()

                    pygame.quit()
                    self.paused_game=False
                    # os.system('python ' + 'menu.py')
                    menu.main()
                            # menu(death_count=0)
                            # pygame.display.flip()

    def showThemes(self):
        global light, dark
        
        themes_image = pygame.image.load("./Mario/graphics/settings.png")
        size = (500, 500)
        themes_image = pygame.transform.scale(themes_image, size)
        themes_rect = themes_image.get_rect()
        themes_rect.center = (screen_width // 2, screen_height // 2)
        self.display_surface.blit(themes_image, themes_rect)
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 180
        button_height = 180
        button_padding = 40
        button_x = (screen_width - button_width) // 2 + 10
        button_y = themes_rect.top + button_padding + 200
        
        # Light themes button
        light_image = pygame.image.load("./Mario/graphics/light.png")
        light_image = pygame.transform.scale(light_image, (button_width, button_height))
        light_button_rect = light_image.get_rect()
        light_button_rect.center = (button_x - 20, button_y - 20)
        self.display_surface.blit(light_image, light_button_rect)
        
        # 'LIGHT' text
        light_text_surface = button_font.render('LIGHT', True, (255, 255, 255))
        light_text_rect = light_text_surface.get_rect()
        light_text_rect.midtop = (light_button_rect.centerx, light_button_rect.bottom + 5)
        self.display_surface.blit(light_text_surface, light_text_rect)
        
        # Dark themes button
        dark_image = pygame.image.load("./Mario/graphics/dark.png")
        dark_image = pygame.transform.scale(dark_image, (button_width, button_height))
        dark_button_rect = dark_image.get_rect()
        dark_button_rect.center = (button_x + 190, button_y - 20)
        self.display_surface.blit(dark_image, dark_button_rect)
        
        # 'DARK' text
        dark_text_surface = button_font.render('DARK', True, (0, 0, 0))
        dark_text_rect = dark_text_surface.get_rect()
        dark_text_rect.midtop = (dark_button_rect.centerx, dark_button_rect.bottom + 5)
        self.display_surface.blit(dark_text_surface, dark_text_rect)
        
        # Back button
        back_button_text = button_font.render("BACK", True, (0, 0, 0))
        back_button_rect = pygame.Rect(button_x, button_y + 180, button_width, 60)
        pygame.draw.rect(self.display_surface, (255, 255, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.display_surface.blit(back_button_text, back_button_text_rect)
        
        # # Close button
        # close_button_rect = pygame.Rect(themes_rect.left + 50, themes_rect.top + 50, 50, 55)
        # pygame.draw.rect(self.display_surface, (0, 0, 0), close_button_rect, border_radius=20)
        # pygame.draw.rect(self.display_surface, (0, 0, 0), close_button_rect, 2, border_radius=20)  # black border
        # close_text = button_font.render("X", True, (255, 255, 255))
        # close_text_rect = close_text.get_rect(center=close_button_rect.center)
        # self.display_surface.blit(close_text, close_text_rect)
        
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
                    if light_button_rect.collidepoint(mouse_pos):
                        print("Light themes button clicked!")
                        self.theme='light'
                        light = True
                        dark = False
                        # unpause()
                        
                        self.sky =Sky(8,'light','level')
                        self.settings_icon = pygame.image.load("./Mario/graphics/gearBlack.png")
                        self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
                        self.settings_rect = self.settings_icon.get_rect()
                        self.settings_rect.topright = (screen_width - 50,15)
                        self.run()
                        self.paused_game = False
                        pygame.display.flip()
                        return
                    elif dark_button_rect.collidepoint(mouse_pos):
                        print("Dark themes button clicked!")
                        self.theme='dark'
                        self.sky =Sky(8,'dark','level')
                        # sky.draw(self.display_surface)
                        self.settings_icon = pygame.image.load("./Mario/graphics/gearWhite.png")
                        self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
                        self.settings_rect = self.settings_icon.get_rect()
                        self.settings_rect.topright = (screen_width - 50,15)
                        
                        self.run()
                        self.paused_game = False
                        light = False
                        dark = True
                        # unpause()
                        pygame.display.flip()
                        return
                    elif back_button_rect.collidepoint(mouse_pos):
                        print("Back button clicked")
                        # paused()
                        self.paused_game=False
                        pygame.display.flip()
                        return
                    # elif close_button_rect.collidepoint(mouse_pos):
                    #     # unpause()
                    #     return
            
            pygame.display.flip()

    
    def htpInGame(self):
        #text box
        text_box_image = pygame.image.load("./Mario/graphics/marioSettings.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (screen_width // 2, screen_height // 2)
        
        # Create a font object
        text_font = pygame.font.Font("Royal Kingdom.ttf", 24)

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

        # Blit the text box surface onto the self.display_surface
        self.display_surface.blit(text_box_image, text_box_image_rect)
        self.display_surface.blit(text_box_surface, (text_box_image_rect.left + 65, text_box_image_rect.top + 65))
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 30)
        button_width = 180
        button_height = 180
        button_padding = 40
        button_x = (screen_width - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Back button
        back_button_text = button_font.render("BACK", True, (0, 0, 0))
        back_button_rect = pygame.Rect(button_x, button_y + 200, button_width, 35)
        pygame.draw.rect(self.display_surface, (255, 255, 255), back_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), back_button_rect, 2, border_radius=20)  # black border
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.display_surface.blit(back_button_text, back_button_text_rect)
        
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
                        self.paused_game = False
                        # paused()
                        pygame.display.update()
                        return
        
            pygame.display.update()

    def exitGame(self):
        #text box
        
        FONT_COLOR = (0,0,0)
        text_box_image = pygame.image.load("Mario/graphics/settings.png")
        size = (500, 500)
        text_box_image = pygame.transform.scale(text_box_image, size)
        text_box_image_rect = text_box_image.get_rect()
        text_box_image_rect.center = (screen_width // 2, screen_height // 2)
        
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

        # Blit the text box surface onto the self.display_surface
        self.display_surface.blit(text_box_image, text_box_image_rect)
        self.display_surface.blit(text_box_surface, (text_box_image_rect.left + 55, text_box_image_rect.top + 90))
        
        # draw buttons
        button_font = pygame.font.Font("Royal Kingdom.ttf", 55)
        button_width = 180
        button_height = 120
        button_padding = 40
        button_x = (screen_width - button_width) // 2 + 10
        button_y = text_box_image_rect.top + button_padding + 200
        
        # Yes button
        yes_button_text = button_font.render("YES", True, FONT_COLOR)
        yes_button_rect = pygame.Rect(button_x - 115, button_y, button_width, button_height)
        pygame.draw.rect(self.display_surface, (255, 255, 255), yes_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), yes_button_rect, 2, border_radius=20)  # black border
        yes_button_text_rect = yes_button_text.get_rect(center=yes_button_rect.center)
        self.display_surface.blit(yes_button_text, yes_button_text_rect)
        
        # No button
        no_button_text = button_font.render("NO", True, FONT_COLOR)
        no_button_rect = pygame.Rect(button_x + 105, button_y, button_width, button_height)
        pygame.draw.rect(self.display_surface, (255, 255, 255), no_button_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), no_button_rect, 2, border_radius=20)  # black border
        no_button_text_rect = no_button_text.get_rect(center=no_button_rect.center)
        self.display_surface.blit(no_button_text, no_button_text_rect)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                    # unpause()
                    self.paused_game = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_button_rect.collidepoint(mouse_pos):
                        # self.create_overworld(self.current_level,self.max_level)
                        self.level_bg_music.stop()
                        menu.main()
                        pygame.display.update()
                        return
                    elif no_button_rect.collidepoint(mouse_pos):
                        # paused()
                        self.paused_game = True
                        pygame.display.update()
                        return
        
            pygame.display.update()
        
    
    def load_gestures(self):

        font_text = pygame.font.Font('Royal Kingdom.ttf',25)
        jump_gesture_text = font_text.render("Jump",True, (255,0,0))
        jump_gesture_text_rect = jump_gesture_text.get_rect()
        jump_gesture_text_rect.topleft =( 350,self.jump_gesture_rect.y+15)
        
        left_hand_gesture_text = font_text.render("Go Right",True, (255,0,0))
        left_hand_gesture_text_rect = left_hand_gesture_text.get_rect()
        left_hand_gesture_text_rect.topleft =( 650,self.leftHandOut_gesture_rect.y+10)
        
        right_hand_gesture_text = font_text.render("Go Left",True, (255,0,0))
        right_hand_gesture_text_rect = right_hand_gesture_text.get_rect()
        right_hand_gesture_text_rect.topleft =(950,self.rightHandThumb_gesture_rect.y+15)


        self.jump_gesture_rect.topright =(350,10)
        self.display_surface.blit(self.jump_gesture,self.jump_gesture_rect)
        self.display_surface.blit(jump_gesture_text,jump_gesture_text_rect)
        self.leftHandOut_gesture_rect.topright = (650,20)
        self.display_surface.blit(self.leftHandOut_gesture,self.leftHandOut_gesture_rect)
        self.display_surface.blit(left_hand_gesture_text,left_hand_gesture_text_rect)
        self.rightHandThumb_gesture_rect.topright = (950,10) 
        self.display_surface.blit(self.rightHandThumb_gesture,self.rightHandThumb_gesture_rect)
        self.display_surface.blit(right_hand_gesture_text,right_hand_gesture_text_rect)

    def run(self):
        
        
        

        # self.tiles.update(self.world_shift) #for shifting the level 
        # self.tiles.draw(self.display_surface)
        self.scroll_x()


        #update the player and then draw it on the self.display_surface
        # self.player.update()
        self.horizointal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        # self.player.draw(self.display_surface)

        #checking scroll


        #decoration
        self.sky.draw(self.display_surface)
        self.cloud.draw(self.display_surface,self.world_shift)
        
        self.display_surface.blit(self.settings_icon, self.settings_rect)
        self.load_gestures()

        #bg_palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #crates
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        #enemis
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        
         
        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)


        #coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        #fg_palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #playerSprites
        self.player.update()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_win()
        self.check_death()

        self.check_coin_collisions()
        self.check_enemy_collisions()
        self.water.draw(self.display_surface,self.world_shift)

        self.pauseGame()
        # self.check_input()
        
        pass