import pygame
from pygame.sprite import *
from config import *
import math
import random
from text import *


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, colorkey):
        sprite = pygame.Surface([width, height])
        sprite.set_colorkey(colorkey)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE // 2
        self.y = y * TILESIZE // 2
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.animation_loop = 0

        self.basic_attack_level = 0
        self.ultimate_attack_level = 0
        self.speed_level = 0
        self.health_and_mana_level = 0

        self.basic_attack_damage = 1 + self.basic_attack_level * 3
        self.ultimate_attack_damage = 5 + self.ultimate_attack_level * 5

        self.image = self.game.character_spritesheet.get_sprite(
            1, 646, self.width, self.height, WHITE
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Animations
        self.up_animations = [
            self.game.character_spritesheet.get_sprite(
                1, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                65, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                129, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                257, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                321, 255, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                385, 255, self.width, self.height, WHITE
            ),
        ]

        self.down_animations = [
            self.game.character_spritesheet.get_sprite(
                1, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                65, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                129, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                257, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                321, 383, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                385, 383, self.width, self.height, WHITE
            ),
        ]

        self.right_animations = [
            self.game.character_spritesheet.get_sprite(
                1, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                65, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                129, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                257, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                321, 444, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                385, 444, self.width, self.height, WHITE
            ),
        ]

        self.left_animations = [
            self.game.character_spritesheet.get_sprite(
                1, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                65, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                129, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                193, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                257, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                321, 321, self.width, self.height, WHITE
            ),
            self.game.character_spritesheet.get_sprite(
                385, 321, self.width, self.height, WHITE
            ),
        ]

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide("x")
        self.rect.y += self.y_change
        self.collide("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.player_speed = PLAYER_SPEED + self.speed_level // 4
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.player_speed

            for sprite in self.game.attacks:
                sprite.rect.x += self.player_speed

            self.x_change -= self.player_speed

            self.facing = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.player_speed
            for sprite in self.game.attacks:
                sprite.rect.x -= self.player_speed

            self.x_change += self.player_speed
            self.facing = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += self.player_speed

            for sprite in self.game.attacks:
                sprite.rect.y += self.player_speed

            self.y_change -= self.player_speed
            self.facing = "up"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.player_speed

            for sprite in self.game.attacks:
                sprite.rect.y -= self.player_speed

            self.y_change += self.player_speed
            self.facing = "down"

    def collide(self, direction):

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.player_speed
                    for sprite in self.game.attacks:
                        sprite.rect.x += self.player_speed
                    self.rect.x = hits[0].rect.left - self.rect.width

                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= self.player_speed
                    for sprite in self.game.attacks:
                        sprite.rect.x -= self.player_speed
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.player_speed
                    for sprite in self.game.attacks:
                        sprite.rect.y += self.player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= self.player_speed
                    for sprite in self.game.attacks:
                        sprite.rect.y -= self.player_speed
                    self.rect.y = hits[0].rect.bottom

    def animate(self):

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 7:
                    self.animation_loop = 1

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2


# BLOCKS
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
        self.width = TILESIZE // 2
        self.image = pygame.transform.scale(self.image, (64, 64))


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


class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.direction = self.game.player.facing
        self.animation_loop = 0
        self.damage = self.game.player.basic_attack_damage
        mouse_position = pygame.mouse.get_pos()

        angle = math.atan2(mouse_position[1] - self.y, mouse_position[0] - self.x)
        self.dx = math.cos(angle) * self.game.player.player_speed
        self.dy = math.sin(angle) * self.game.player.player_speed

        self.image = self.game.attack_spritesheet.get_sprite(
            0, 0, self.width, self.height, BLACK
        )

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animations = [
            self.game.attack_spritesheet.get_sprite(
                20, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                80, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                140, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                200, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                265, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                330, 30, self.width, self.height * 0.75, BLACK
            ),
            self.game.attack_spritesheet.get_sprite(
                390, 30, self.width, self.height * 0.75, BLACK
            ),
        ] * (self.game.player.speed_level + 1)
        self.upgrade_attack_tier(self.game.player.basic_attack_level // 3)

    def update(self):
        self.collide()
        self.movement()
        self.animate()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for sprite in hits:
                sprite.health -= self.damage
                self.kill()
                Temporary_text_damage(
                    self.game,
                    self.damage,
                    "red",
                    sprite.rect.x,
                    sprite.rect.y + 32,
                    pygame.font.Font(
                        "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                    ),
                )

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= len(self.animations):
            self.kill()

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)

    def upgrade_attack_tier(self, tier):
        if tier == 1:
            self.animations = [
                self.game.attack_spritesheet.get_sprite(
                    0, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    64, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    128, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    192, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    256, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    320, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    384, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    448, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    512, 84, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    576, 84, self.width, self.height * 0.75, BLACK
                ),
            ] * (self.game.player.speed_level + 1)
        if tier == 2:
            self.animations = [
                self.game.attack_spritesheet.get_sprite(
                    0, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    64, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    128, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    192, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    256, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    320, 148, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    384, 148, self.width, self.height * 0.75, BLACK
                ),
            ] * (self.game.player.speed_level + 1)
        if tier >= 3:
            self.animations = [
                self.game.attack_spritesheet.get_sprite(
                    0, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    64, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    128, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    192, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    256, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    320, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    384, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    448, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    512, 212, self.width, self.height * 0.75, BLACK
                ),
                self.game.attack_spritesheet.get_sprite(
                    576, 212, self.width, self.height * 0.75, BLACK
                ),
            ] * (self.game.player.speed_level + 1)


class Ultimate_attack(Attack):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.width *= 2
        self.height *= 2
        self.animations = [
            self.game.ultimate_attack_spritesheet.get_sprite(
                0, 0, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                128, 0, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                256, 0, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                384, 0, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                0, 128, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                128, 128, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                256, 128, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                384, 128, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                0, 256, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                128, 256, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                256, 256, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                384, 256, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                0, 384, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                128, 384, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                256, 384, self.width, self.height, BLACK
            ),
            self.game.ultimate_attack_spritesheet.get_sprite(
                384, 384, self.width, self.height, BLACK
            ),
        ]

        self.upgrade_attack_tier(self.game.player.ultimate_attack_level // 3)
        self.image = self.animations[0]
        self.damage = (
            self.game.player.ultimate_attack_damage
            + self.game.player.ultimate_attack_level * 5
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def upgrade_attack_tier(self, tier):

        if tier == 1:
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (256, 256)
                )
            self.height *= 2
            self.width *= 2

        elif tier == 2:

            self.game.ultimate_attack_spritesheet = Spritesheet(
                "images/missles/lightningclaw.png"
            )

            self.animations = [
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 0, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 0, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 0, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 0, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 128, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 128, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 128, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 128, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 256, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 256, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 256, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 256, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 384, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 384, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 384, self.width, self.height, BLACK
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 384, self.width, self.height, BLACK
                ),
            ]
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (256, 256)
                )
            self.height *= 2
            self.width *= 2

        elif tier >= 3:
            self.game.ultimate_attack_spritesheet = Spritesheet(
                "images/missles/ultimate_tornado_thunderclaw.png"
            )

            self.animations = [
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 0, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 0, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 0, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 0, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 128, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 128, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 128, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 128, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 256, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 256, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 256, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 256, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    0, 384, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    128, 384, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    256, 384, self.width, self.height, WHITE
                ),
                self.game.ultimate_attack_spritesheet.get_sprite(
                    384, 384, self.width, self.height, WHITE
                ),
            ]
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (512, 512)
                )
            self.height *= 4
            self.width *= 4

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for sprite in hits:
                sprite.health -= self.damage
                Temporary_text_damage(
                    self.game,
                    self.damage,
                    "blue",
                    sprite.rect.x,
                    sprite.rect.y + 32,
                    pygame.font.Font(
                        "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                    ),
                )

    def animate(self):

        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 16:
            self.kill()

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx) * 2
        self.rect.y = self.rect.y + int(self.dy) * 2


class Enemy_attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y, enemy):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.enemy = enemy
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.direction = random.choice(["left", "right", "down", "up"])
        self.damage = self.enemy.damage

        angle = math.atan2(
            self.game.player.rect.y - self.y, self.game.player.rect.x - self.x
        )
        self.dx = math.cos(angle) * self.enemy.speed * 2
        self.dy = math.sin(angle) * self.enemy.speed * 2

        self.spritesheet = self.enemy.enemy_attack_spritesheet

        self.personalize(self.enemy.name)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def personalize(self, name):
        if name == "Grey Mouse":
            self.image = self.spritesheet.get_sprite(
                0, 0, self.width, self.height // 2, WHITE
            )
            self.image = pygame.transform.scale(self.image, (16, 8))
            self.animations = [
                pygame.transform.rotate(self.image, 15 * i) for i in range(1, 25)
            ]

        if name == "Brown Mouse":
            self.image = self.spritesheet.get_sprite(0, 0, 16, 8, WHITE)
            self.image = pygame.transform.scale(self.image, (32, 16))
            self.animations = [
                pygame.transform.rotate(self.image, 15 * i) for i in range(1, 25)
            ]
            print(self.animations)

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        if hits:
            for sprite in hits:
                if sprite.__class__.__name__ == "Player":
                    self.game.health_bar.lose(self.damage)
                    self.kill()

    def update(self):
        self.collide()
        self.movement()
        self.animate()

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.15
        if self.animation_loop >= len(self.animations):
            self.kill()

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx) * 2
        self.rect.y = self.rect.y + int(self.dy) * 2


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        game,
        x,
        y,
        enemy_spritesheet_path,
        enemy_attack_spritesheet_path,
        name,
        damage,
        health,
        exp,
        speed,
    ):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.height, self.width = TILESIZE, TILESIZE

        self.facing = random.choice(["up", "down", "right", "left"])
        self.animation_loop = 0
        enemy_spritesheet = Spritesheet(enemy_spritesheet_path)
        self.enemy_attack_spritesheet = Spritesheet(enemy_attack_spritesheet_path)

        self.image = enemy_spritesheet.get_sprite(
            1, 128, self.width, self.height, WHITE
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = speed
        self.name = name
        self.damage = damage
        self.health = health
        self.experience = exp
        self.shoot_cooldown_count = 0
        self.up_animations = [
            enemy_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(64, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(128, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(192, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(256, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(320, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(384, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(448, 0, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(512, 0, self.width, self.height, WHITE),
        ]

        self.down_animations = [
            enemy_spritesheet.get_sprite(0, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(64, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(128, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(192, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(256, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(320, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(384, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(448, 128, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(512, 128, self.width, self.height, WHITE),
        ]

        self.right_animations = [
            enemy_spritesheet.get_sprite(0, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(64, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(128, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(192, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(256, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(320, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(384, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(448, 192, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(512, 192, self.width, self.height, WHITE),
        ]

        self.left_animations = [
            enemy_spritesheet.get_sprite(0, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(64, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(128, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(192, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(256, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(320, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(384, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(448, 64, self.width, self.height, WHITE),
            enemy_spritesheet.get_sprite(512, 64, self.width, self.height, WHITE),
        ]
        self.attack = self.enemy_attack_spritesheet.get_sprite(0, 0, 64, 32, BLACK)

    def draw(self, screen):
        pass

    def update(self):

        self.cooldown()
        self.movement()
        self.animate()
        self.collide("x")
        self.collide("y")
        self.check_health()
        self.attack_player()

    def collide(self, direction):

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.facing == "right":
                    self.rect.x = hits[0].rect.left - self.rect.width

                if self.facing == "left":
                    self.rect.x = hits[0].rect.right + self.rect.width

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.facing == "up":
                    self.rect.y = hits[0].rect.down - self.rect.height

                if self.facing == "down":
                    self.rect.y = hits[0].rect.down + self.rect.height

    def attack_player(self):

        if self.shoot_cooldown_count == 0 and self.dist < 750:
            self.shoot_cooldown_count += 1
            if self.facing == "up":
                Enemy_attack(self.game, self.rect.x, self.rect.y - TILESIZE // 2, self)
            if self.facing == "down":
                Enemy_attack(self.game, self.rect.x, self.rect.y + TILESIZE // 2, self)
            if self.facing == "left":
                Enemy_attack(self.game, self.rect.x - TILESIZE // 2, self.rect.y, self)
            if self.facing == "right":
                Enemy_attack(self.game, self.rect.x + TILESIZE // 2, self.rect.y, self)

    def movement(self):
        self.x_change = 0
        self.y_change = 0
        dx, dy = (
            self.game.player.rect.x - self.rect.x,
            self.game.player.rect.y - self.rect.y,
        )
        self.dist = math.hypot(dx, dy)
        if self.dist < 750:
            if self.game.player.rect.x > self.rect.x:

                self.rect.x += self.speed
                self.facing = "right"
                self.x_change = 1

            elif self.game.player.rect.x < self.rect.x:

                self.rect.x -= self.speed
                self.facing = "left"
                self.x_change = 1

            elif self.game.player.rect.y > self.rect.y:

                self.rect.y += self.speed
                self.facing = "down"
                self.y_change = 1

            elif self.game.player.rect.y < self.rect.y:

                self.rect.y -= self.speed
                self.facing = "up"
                self.y_change = 1

    def animate(self):

        if self.dist < 750:
            if self.facing == "down":

                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1

            if self.facing == "up":

                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1

            if self.facing == "left":

                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1

            if self.facing == "right":

                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.15
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        else:
            if self.facing == "up":
                self.image = self.up_animations[0]
            elif self.facing == "down":
                self.image = self.down_animations[0]
            elif self.facing == "right":
                self.image = self.right_animations[0]
            else:
                self.image = self.left_animations[0]

    def check_health(self):
        if self.health <= 0:
            self.kill()
            self.game.experience_bar.get(self.experience)
            Temporary_text_experience(
                self.game,
                f"+{self.experience} xp",
                "yellow",
                self.game.experience_bar.x + 325,
                self.game.experience_bar.y + 12,
                pygame.font.Font("font/pixel_font.ttf", 12),
            )

    def cooldown(self):
        if self.shoot_cooldown_count >= 150:
            self.shoot_cooldown_count = 0
        elif self.shoot_cooldown_count > 0:
            self.shoot_cooldown_count += 1


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
        ratio = self.remaining / self.full
        pygame.draw.rect(screen, self.color_2, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color_1, (self.x, self.y, self.w * ratio, self.h))
        Text(
            f"{math.floor(self.remaining)}/{self.full}",
            BLACK,
            self.x + 150,
            self.y + 12,
            pygame.font.Font("font/pixel_font.ttf", 12),
        ).draw(screen)
        for i in range(4):
            pygame.draw.rect(
                screen, (0, 0, 0), (self.x - i, self.y - i, self.w, self.h), 1
            )


class Health_bar(Bar):
    def __init__(self, game, x, y, w, h, full, bg, fg):
        super().__init__(game, x, y, w, h, full, bg, fg)

    def lose(self, amount):
        if self.remaining > 0:
            self.remaining -= amount
        if self.remaining <= 0:
            self.remaining = 0
            self.game.player.kill()
            self.game.active_game = False


class Exp_bar(Bar):
    def __init__(self, game, x, y, w, h, full, bg, fg):
        super().__init__(game, x, y, w, h, full, bg, fg)
        self.remaining = 0

    def lose(self):
        self.full = int(self.full * 1.5)

    def get(self, amount):
        if self.remaining < self.full:
            self.remaining += amount
        if self.remaining >= self.full:
            self.game.paused_game = True
            self.remaining = self.remaining - self.full
            self.lose()


class Skill_up_bar(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, current, full, bg, fg):
        self.game = game
        self.groups = self.game.text
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.current = current
        self.full = full
        self.color_1 = fg
        self.color_2 = bg

    def update(self):
        self.draw(self.game.screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_2, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(
            screen,
            self.color_1,
            (self.x, self.y, self.w * self.current // self.full, self.h),
        )
        for i in range(4):
            pygame.draw.rect(
                screen, (0, 0, 0), (self.x - i, self.y - i, self.w, self.h), 1
            )
        for j in range(self.full):
            for i in range(4):
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (
                        self.x + (self.w // self.full) * j,
                        self.y - i,
                        self.w // self.full,
                        self.h,
                    ),
                    1,
                )


class Cursor:
    def __init__(self, game) -> None:
        self.game = game
        self.image = pygame.transform.scale(
            self.game.cursor_spritesheet.get_sprite(0, 0, 968, 1408, (48, 54, 66)),
            (16, 32),
        )

        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
