import pygame
import os
import sys
from config import *
from entities import *
from text import Text 
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 30)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('font/pixel_font.ttf', 50)
        self.sky_surface = pygame.image.load('images/backgrounds/clouds.jpg')
        self.ground_surface = pygame.image.load('images/backgrounds/ground.png')
        self.window_open = True
        self.active_game = False
        self.start_button = Text("START", AZURE, 400, 100, self.font) 
        self.exit_button = Text("EXIT", DARK_GREY, 400, 200, self.font) 
        self.intro_screen()
        self.cursor_spritesheet = Spritesheet('images/cursor/cursor.jpg')
        self.shoot_cooldown_count = 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.character_spritesheet = Spritesheet('images/player/player.png')
        self.terrain_spritesheet = Spritesheet('images/terrain/terrain.png')
        self.attack_spritesheet = Spritesheet('images/missles/spikes.png')
        self.ultimate_attack_spritesheet = Spritesheet('images/missles/tornado.png')
        
        pygame.mouse.set_visible(False)
        self.cursor = Cursor(self)
        
        
        
    def create_tilemap(self):
        """
        B - BLock 
        P - Player
        O - Object(Tree, water sticks etc.)     
        D - Decorations   
        W - Water
        T - trail
        """
        
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                random_terrain = random.randint(0,2)
                if i < 49: 
                    
                    
                    if random_terrain == 1:
                        Ground(self, j, i, (self.terrain_spritesheet.get_sprite(64, 352, 32, 32, WHITE), (64,64)))
                    elif random_terrain == 2:
                        Ground(self, j, i, (self.terrain_spritesheet.get_sprite(96, 352, 32, 32, WHITE), (64,64)))
                        
                    else:
                        Ground(self, j, i, (self.terrain_spritesheet.get_sprite(1, 352, 32, 32, WHITE), (64,64)))
                        
                    if column == "T":
                        Ground(self, j, i, (self.terrain_spritesheet.get_sprite(27, 89, 32, 32, WHITE), (64,64)))
                    elif column == "O":
                        Block(self, j, i, (self.terrain_spritesheet.get_sprite(43, 832, 64, 64, BLACK), (64, 64)))
                    if column == "D":
                            Block(self, j, i, (self.terrain_spritesheet.get_sprite(96, 192, 32, 64, BLACK), (32, 64)))
                           
                    elif column == "B":
                        Boundary_blocks(self, j, i, (self.terrain_spritesheet.get_sprite(994, 640, 32, 64, BLACK), (128, 64)))
                    elif column == "P":  
                        self.player = Player(self, j, i)
                    elif column == "E":
                        Enemy(self, j, i, "Grey Mouse", 5, 10)
                    elif column == "W":
                        Block(self, j, i, (self.terrain_spritesheet.get_sprite(891,90, 32, 32, WHITE), (64, 64)))
                        
                else:
                    Ground(self, j, i, (self.terrain_spritesheet.get_sprite(64, 352, 32, 32, WHITE), (64,64)))
                    if column == "B":
                        Boundary_blocks(self, j, i, (self.terrain_spritesheet.get_sprite(994, 640, 32, 64, BLACK), (64, 64)))
                    
        self.health_bar = Bar(self, 10, 10, 300, 30, 10, "red", "green")
        self.mana_bar = Bar(self, 10, 60, 300, 30, 10, "grey", LIGHTBLUE)
        self.experience_bar = Exp_bar(self, 10, 105, 300, 30, 10, "grey", "yellow")       
        
    
    def new(self):
       
        self.active_game = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        self.create_tilemap()
        
    def events_main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.active_game = False
                self.window_open = False
                
            if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.start_button.color = AZURE
                self.exit_button.color =  DARK_GREY
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.active_game = True
                    
            else:
                self.start_button.color = DARK_GREY
                self.exit_button.color = AZURE
          
            if self.exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.start_button.color = DARK_GREY
                self.exit_button.color = AZURE
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pygame.quit()
                    sys.exit()
                    
            else:
                self.start_button.color = AZURE
                self.exit_button.color = DARK_GREY
                
    def events_in_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active_game = False
                self.window_open = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and self.shoot_cooldown_count == 0:
                
                if event.button == 1:
                    self.shoot_cooldown_count += 1 
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x  - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x  + TILESIZE, self.player.rect.y)    
                        
            if event.type == pygame.MOUSEBUTTONDOWN and self.mana_bar.remaining >= 10:
                if event.button == 3:
                    self.mana_bar.lose(10)
                    
                    if self.player.facing == 'up':
                        Ultimate_attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Ultimate_attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Ultimate_attack(self, self.player.rect.x  - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Ultimate_attack(self, self.player.rect.x  + TILESIZE, self.player.rect.y)    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.experience_bar.get(5)
    def cooldown(self):
        if self.shoot_cooldown_count >= 50:
            self.shoot_cooldown_count = 0 
        elif self.shoot_cooldown_count > 0:
            self.shoot_cooldown_count+=1
        if self.mana_bar.remaining != self.mana_bar.full:
            self.mana_bar.get()
        if self.health_bar.remaining != self.health_bar.full:
            self.health_bar.get()
        
            
    def update(self):
        
        self.cooldown()
        self.all_sprites.update()
        self.attacks.update()
        self.health_bar.update()
        self.mana_bar.update()
        self.experience_bar.update()
        self.cursor.update()
        
        
        
        
    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.attacks.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.mana_bar.draw(self.screen)
        self.experience_bar.draw(self.screen)
        self.cursor.draw(self.screen)
        
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        while self.active_game:
            
            self.events_in_game()
            self.update()
            self.draw()
        self.window_open = False
        
    def game_over(self):
        print('Game Over')
    
    def intro_screen(self):
        self.screen = pygame.display.set_mode((800, 400))
        sky_x_position = 600
        
        while not self.active_game:
            
            self.screen.fill(LIGHTBLUE)
            self.screen.blit(self.sky_surface, (sky_x_position,0))        
            self.screen.blit(self.ground_surface, (0, 300))
            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            sky_x_position -= 2
            if sky_x_position <= -1200:
                sky_x_position = 700
            self.events_main_menu()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def pause_screen(self):
        pass
        
if __name__ == "__main__":
    
    game = Game()
    game.new()
    while game.window_open:
        game.main()
        game.game_over()


    pygame.quit()
    sys.exit()

