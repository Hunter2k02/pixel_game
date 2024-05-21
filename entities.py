import pygame
from pygame.sprite import *
from config import * 
import math 
import random 
from text import Text 

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height, colorkey):
        sprite = pygame.Surface([width, height])
        sprite.set_colorkey(colorkey)
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        self.game = game 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites 
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.flag = 1
        self.x = x * TILESIZE//2
        self.y = y * TILESIZE//2
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'down'
        
        self.animation_loop = 0
        
        self.image = self.game.character_spritesheet.get_sprite(1, 646, self.width, self.height, WHITE) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y
        
        #Attributes
        
        
        
    def level_up(self, option):
        if option == 1:
            print("Basic attacks lvl up!")
        elif option == 2:
            print("Ultimate attacks lvl up!")
        elif option == 3:
            print("Mobility lvl up!")
        else:
            print("Endurance lvl up!")
            
        
    def update(self):
        
        self.movement()
        self.animate()
        self.rect.x += self.x_change 
        self.collide('x')
        self.rect.y += self.y_change
        self.collide('y')
        
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED 
                
            for sprite in self.game.attacks:
                sprite.rect.x += PLAYER_SPEED
                
            self.x_change -= PLAYER_SPEED
            
            self.facing = 'left'
            
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            for sprite in self.game.attacks:
                sprite.rect.x -= PLAYER_SPEED
                
            
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
                
            for sprite in self.game.attacks:
                    sprite.rect.y += PLAYER_SPEED
                
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            
              
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
                
            for sprite in self.game.attacks:
                    sprite.rect.y -= PLAYER_SPEED
            
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
    
        
        
    def collide(self, direction):
        self.flag = 0
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED 
                    self.rect.x = hits[0].rect.left - self.rect.width
                    
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right 
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom            
                    
            
    def animate(self):
        up_animations = [
                            self.game.character_spritesheet.get_sprite(1, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(65, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(129, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(257, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(321, 255, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(385, 255, self.width, self.height, WHITE),
                           ]
        
        down_animations = [
                            self.game.character_spritesheet.get_sprite(1, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(65, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(129, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(257, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(321, 383, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(385, 383, self.width, self.height, WHITE),
                           ]
        
        right_animations = [
                            self.game.character_spritesheet.get_sprite(1, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(65, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(129, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(257, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(321, 444, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(385, 444, self.width, self.height, WHITE),
                           ]
        
        left_animations = [
                            self.game.character_spritesheet.get_sprite(1, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(65, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(129, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(193, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(257, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(321, 321, self.width, self.height, WHITE),
                            self.game.character_spritesheet.get_sprite(385, 321, self.width, self.height, WHITE),
                           ]
        
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = down_animations[0]
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1 
                    
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_animations[0]
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1 
                    
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = left_animations[0]
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1             
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_animations[0]
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1 
                
    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2
#BLOCKS    
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, Spritesheet):
        
        self.game = game 
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE 
        self.y = y * TILESIZE 
        self.width = TILESIZE 
        self.height = TILESIZE
        
        self.image = pygame.transform.scale(Spritesheet[0], Spritesheet[1])
        
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
class Boundary_blocks(Block):
    def __init__(self, game, x, y, Spritesheet):
        Block.__init__(self, game, x, y, Spritesheet)
        self.width = TILESIZE //2
        self.image = pygame.transform.scale(self.image, (64,64))
        
        
        
        
        
        
        
#Grounds 
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, Spritesheet):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE 
        self.height = TILESIZE
        
        self.image = pygame.transform.scale(Spritesheet[0], Spritesheet[1])
        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y


#Attacks

class Attack(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y):
        self.game = game 
        self._layer = PLAYER_LAYER
        self.groups =  self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y 
        self.width = TILESIZE
        self.height = TILESIZE
        self.direction = self.game.player.facing
        self.animation_loop = 0 
        
        mouse_position = pygame.mouse.get_pos()
        
        angle = math.atan2(mouse_position[1] - self.y, mouse_position[0] - self.x)
        self.dx = math.cos(angle)*PLAYER_SPEED
        self.dy = math.sin(angle)*PLAYER_SPEED
        
        
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
        
    def update(self):
        self.movement()
        self.animate()
        self.colide()
    
    def colide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
    def animate(self):
        
        animations = [self.game.attack_spritesheet.get_sprite(20, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(80, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(140, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(200, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(265, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(330, 30, self.width, self.height*0.75, BLACK),
                         self.game.attack_spritesheet.get_sprite(390, 30, self.width, self.height*0.75, BLACK),
                         ]*2
        
        
        
        
            
        self.image = animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1 
        if self.animation_loop >= 14:
            self.kill()
                
    def movement(self):
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, damage, health):
        self.game = game 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.height, self.width = TILESIZE, TILESIZE
        self.x_change, self.y_change = 0, 0
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 0
        
        
        self.name = name
        self.damage = damage 
        self.health = health 
        
        self.grey_mouse_child_spritesheet = Spritesheet('images/enemies/level_1/grey_mouse_child.png')
    
    def update(self):
        # self.movement()
        self.animate()
        # self.colide()
        
    def colide(self):
        hits = pygame.sprite.spritecollide(self, self.game.player, False)
        
    def movement(self):
        pass

    def animate(self):
        up_animations = [
                                self.grey_mouse_child_spritesheet.get_sprite(1,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(65,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(129,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(257,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(321,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(385,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(449,521, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(513,521, self.width, self.height, WHITE)
                               ]

        down_animations = [
                                self.grey_mouse_child_spritesheet.get_sprite(1,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(65,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(129,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(257,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(321,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(385,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(449,654, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(513,654, self.width, self.height, WHITE)
                               ]

        right_animations = [
                                self.grey_mouse_child_spritesheet.get_sprite(1, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(65, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(129, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(257, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(321, 724, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(385, 724, self.width, self.height, WHITE),
                               ]

        left_animations = [
                                self.grey_mouse_child_spritesheet.get_sprite(1, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(65, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(129, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(193, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(257, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(321, 590, self.width, self.height, WHITE),
                                self.grey_mouse_child_spritesheet.get_sprite(385, 590, self.width, self.height, WHITE),
                               ]


        if self.facing == 'down':
            if self.y_change == 0:
                self.image = down_animations[0]
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1 

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_animations[0]
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1 

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = left_animations[0]
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1             

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_animations[0]
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1 
                
class Ultimate_attack(Attack):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.width *= 2 
        self.height *= 2
        self.animations = [self.game.ultimate_attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(128, 0, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(256, 0, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(384, 0, self.width, self.height,BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(0, 128, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(128, 128, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(256, 128, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(384, 128, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(0, 256, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(128, 256, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(256, 256, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(384, 256, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(0, 384, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(128, 384, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(256, 384, self.width, self.height, BLACK),
                                   self.game.ultimate_attack_spritesheet.get_sprite(384, 384, self.width, self.height, BLACK),
                         ]
        self.image = self.animations[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
        
        
    def animate(self):
        
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1 
        if self.animation_loop >= 16:
            self.kill()
            
    def movement(self):
        self.rect.x = self.rect.x + int(self.dx) * 2 
        self.rect.y = self.rect.y + int(self.dy) * 2 
        

    
    
class Bar(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, full, bg, fg):
        self.game = game
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h 
        self.remaining = 10
        self.full = full
        self.regen = 0.01
        self.color_1 = fg 
        self.color_2 = bg
    
    def update(self):
        self.draw(self.game.screen)
    
    def lose(self, amount):
        if self.remaining > 0:
            self.remaining -= amount
        if self.remaining <= 0:
            self.remaining = 0
        
            
    def get(self):
        if self.remaining < self.full:
            self.remaining += self.regen
        if self.remaining >= self.full:
            self.remaining = self.full
        
    def draw(self, screen):
        ratio = self.remaining/self.full
        pygame.draw.rect(screen, self.color_2, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color_1, (self.x, self.y, self.w*ratio, self.h))
        Text(f"{math.floor(self.remaining)}/{self.full}", BLACK, self.x+150, self.y+12, pygame.font.Font('font/pixel_font.ttf', 12)).draw(screen)
        for i in range(4):
            pygame.draw.rect(screen, (0,0,0), (self.x-i,self.y-i,self.w,self.h), 1)
    
class Exp_bar(Bar):
    def __init__(self, game, x, y, w, h, full, bg, fg):
        super().__init__(game, x, y, w, h, full, bg, fg)
        self.remaining=0
        
    def lose(self):
        self.game.player.level_up(random.randint(0,4))
        self.remaining=0
        self.full = int(self.full * 1.5)
        
    def get(self, amount):
        if self.remaining < self.full:
            self.remaining += amount
        if self.remaining >= self.full:
            self.remaining = self.remaining - self.full
            self.lose()
        
        
        

        

        
        
        
        
        

class Cursor:
    def __init__(self, game) -> None:
        self.game = game 
        self.image = pygame.transform.scale(self.game.cursor_spritesheet.get_sprite(0, 0, 968, 1408, (48, 54, 66)), (16, 32))
        
        
        self.x = 0
        self.y = 0
        
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        self.x = pygame.mouse.get_pos()[0] 
        self.y = pygame.mouse.get_pos()[1] 