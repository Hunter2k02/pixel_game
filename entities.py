import pygame
from pygame.sprite import *
from config import *
import math
import random
from text import *


class Spritesheet:
    """
    A class representing a spritesheet.

    Attributes:
        sheet (pygame.Surface): The spritesheet image.

    Methods:
        __init__(self, file): Initializes the Spritesheet object.
        get_sprite(self, x, y, width, height, colorkey): Extracts a sprite from the spritesheet.

    """

    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, colorkey):
        """
        Extracts a sprite from the spritesheet.

        Args:
            x (int): The x-coordinate of the top-left corner of the sprite.
            y (int): The y-coordinate of the top-left corner of the sprite.
            width (int): The width of the sprite.
            height (int): The height of the sprite.
            colorkey (tuple): The color key used for transparency.

        Returns:
            pygame.Surface: The extracted sprite.

        """
        sprite = pygame.Surface([width, height])
        sprite.set_colorkey(colorkey)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite


class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Attributes:
        game (Game): The instance of the Game class.
        x (int): The x-coordinate of the player's position.
        y (int): The y-coordinate of the player's position.
        width (int): The width of the player's sprite.
        height (int): The height of the player's sprite.
        absolute_sprite_moved_value (tuple): The absolute value of the player's sprite movement.
        x_change (int): The change in x-coordinate of the player's position.
        y_change (int): The change in y-coordinate of the player's position.
        facing (str): The direction the player is facing.
        animation_loop (int): The current animation loop count.
        level (int): The player's level.
        basic_attack_level (int): The level of the player's basic attack.
        ultimate_attack_level (int): The level of the player's ultimate attack.
        speed_level (int): The level of the player's speed.
        health_and_mana_level (int): The level of the player's health and mana.
        basic_attack_damage (int): The damage of the player's basic attack.
        ultimate_attack_damage (int): The damage of the player's ultimate attack.
        image (Surface): The image of the player's sprite.
        rect (Rect): The rectangle representing the player's position and size.
        player_speed (int): The speed of the player's movement.
        up_animations (list): The list of up-facing animation frames.
        down_animations (list): The list of down-facing animation frames.
        right_animations (list): The list of right-facing animation frames.
        left_animations (list): The list of left-facing animation frames.
    Methods:
        update(self): Updates the player's position and sprite.
        movement(self, keys): Moves the player based on the keys pressed.
        collide(self, direction): Checks for collisions with blocks.
        animate(self): Animates the player's sprite based on the direction they are facing.
        get_center(self): Returns the center of the player's sprite.
    """

    def __init__(self, game, x: int, y: int):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.absolute_sprite_moved_value = (0, 0)
        self.music = [0, 0, 0, 0]
        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.animation_loop = 0

        self.level = 1
        self.basic_attack_level = 0
        self.ultimate_attack_level = 0
        self.speed_level = 0
        self.health_and_mana_level = 0

        self.basic_attack_damage = 2 + self.level + self.basic_attack_level * 3
        self.ultimate_attack_damage = (
            5 + self.level * 3 + self.ultimate_attack_level * 5
        )

        self.image = self.game.character_spritesheet.get_sprite(
            1, 646, self.width, self.height, WHITE
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.player_speed = PLAYER_SPEED + self.speed_level // 4
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

    def change_music(self):
        if (
            self.music[0] == 0
            and self.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.absolute_sprite_moved_value[1] / 69268 // 16 > -37
        ):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.game.music.play_music("level_1")
            pygame.mixer.music.set_volume(0.08)
            self.music[0], self.music[1], self.music[2], self.music[3] = 1, 0, 0, 0

        elif (
            self.music[1] == 0
            and self.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.absolute_sprite_moved_value[1] / 69268 // 16 < -36
            and self.absolute_sprite_moved_value[1] / 69268 // 16 > -54
        ):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.game.music.play_music("level_2")
            pygame.mixer.music.set_volume(0.08)
            self.music[0], self.music[1], self.music[2], self.music[3] = 0, 1, 0, 0

        elif (
            self.music[2] == 0
            and self.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.absolute_sprite_moved_value[1] / 69268 // 16 < -54
        ):

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.game.music.play_music("level_3")
            pygame.mixer.music.set_volume(0.08)
            self.music[0], self.music[1], self.music[2], self.music[3] = 0, 0, 1, 0
        elif (
            self.music[3] == 0
            and self.absolute_sprite_moved_value[0] / 69268 // 16 < -80
        ):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.game.music.play_music("boss_room")
            pygame.mixer.music.set_volume(0.08)
            self.music[0], self.music[1], self.music[2], self.music[3] = 0, 0, 0, 1

    def update(self):
        """
        Updates the player's position and sprite.
        """
        self.change_music()
        keys = pygame.key.get_pressed()
        if keys:
            self.movement(keys)
            self.animate()
            self.animate()
            self.rect.x += self.x_change
            self.collide("x")
            self.rect.y += self.y_change
            self.collide("y")

            self.x_change = 0
            self.y_change = 0

    def movement(self, keys):
        """
        Move the player and update the sprite positions based on the keys pressed.

        Args:
            keys (dict): A dictionary containing the state of all keyboard keys.

        Returns:
            None
        """

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.player_speed
                # Update the absolute value of the player's sprite movement
                self.absolute_sprite_moved_value = (
                    self.absolute_sprite_moved_value[0] + self.player_speed,
                    self.absolute_sprite_moved_value[1],
                )

            for sprite in self.game.attacks:
                sprite.rect.x += self.player_speed

            self.x_change -= self.player_speed
            self.facing = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Move all the sprites to the left
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.player_speed
                self.absolute_sprite_moved_value = (
                    self.absolute_sprite_moved_value[0] - self.player_speed,
                    self.absolute_sprite_moved_value[1],
                )
            # Move the attacks relative to the player
            for sprite in self.game.attacks:
                sprite.rect.x -= self.player_speed
            # Update the player's x-coordinate by sprite movement
            self.x_change += self.player_speed
            self.facing = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += self.player_speed
                self.absolute_sprite_moved_value = (
                    self.absolute_sprite_moved_value[0],
                    self.absolute_sprite_moved_value[1] + self.player_speed,
                )

            for sprite in self.game.attacks:
                sprite.rect.y += self.player_speed

            self.y_change -= self.player_speed
            self.facing = "up"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.player_speed
                self.absolute_sprite_moved_value = (
                    self.absolute_sprite_moved_value[0],
                    self.absolute_sprite_moved_value[1] - self.player_speed,
                )

            for sprite in self.game.attacks:
                sprite.rect.y -= self.player_speed

            self.y_change += self.player_speed
            self.facing = "down"

    def collide(self, direction):
        # https://stackoverflow.com/questions/20180594/pygame-collision-by-sides-of-sprite
        """
        Attribute:
            direction (str): The direction of the collision.
        Description:
            Checks for collisions with blocks.
        """
        # Check for collisions with blocks on x-axis
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # If the player is moving to the right
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.player_speed
                        # Update the absolute value of the player's sprite movement when colliding with blocks
                        self.absolute_sprite_moved_value = (
                            self.absolute_sprite_moved_value[0] + self.player_speed,
                            self.absolute_sprite_moved_value[1],
                        )
                    for sprite in self.game.attacks:
                        sprite.rect.x += self.player_speed
                    self.rect.x = hits[0].rect.left - self.rect.width

                # If the player is moving to the left
                if self.x_change < 0:

                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= self.player_speed
                        self.absolute_sprite_moved_value = (
                            self.absolute_sprite_moved_value[0] - self.player_speed,
                            self.absolute_sprite_moved_value[1],
                        )
                    for sprite in self.game.attacks:
                        sprite.rect.x -= self.player_speed
                    self.rect.x = hits[0].rect.right
        # Check for collisions with blocks on y-axis
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # If the player is moving down
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.player_speed

                        self.absolute_sprite_moved_value = (
                            self.absolute_sprite_moved_value[0],
                            self.absolute_sprite_moved_value[1] + self.player_speed,
                        )
                    for sprite in self.game.attacks:
                        sprite.rect.y += self.player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                # If the player is moving up
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= self.player_speed
                        self.absolute_sprite_moved_value = (
                            self.absolute_sprite_moved_value[0],
                            self.absolute_sprite_moved_value[1] - self.player_speed,
                        )
                    for sprite in self.game.attacks:
                        sprite.rect.y -= self.player_speed
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        """
        Animates the player's sprite based on the direction they are facing.
        """
        if self.facing == "down":
            if self.y_change == 0:
                # If the player is not moving, display the first frame of the down-facing animation
                self.image = self.down_animations[0]
            else:
                # If the player is moving, display the animation frames
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
    """
    Represents a block in the game.

    Attributes:
        game (Game): The game instance.
        x (int): The x-coordinate of the block.
        y (int): The y-coordinate of the block.
        Spritesheet (list): The spritesheet used for the block.

    """

    def __init__(self, game, x, y, Spritesheet):
        """
        Initializes a new instance of the Block class.

        Args:
            game (Game): The game instance.
            x (int): The x-coordinate of the block.
            y (int): The y-coordinate of the block.
            Spritesheet (list): The spritesheet used for the block.

        """
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
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))


class Ground(pygame.sprite.Sprite):
    """
    A class representing the ground in the game.

    Attributes:
        game (Game): The instance of the Game class.
        x (int): The x-coordinate of the ground.
        y (int): The y-coordinate of the ground.
        Spritesheet[0] (Surface): The spritesheet used for the ground.
        Spritesheet[1] (tuple): The size of the ground.
    """

    def __init__(self, game, x, y, Spritesheet):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.id = (x, y)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.transform.scale(Spritesheet[0], Spritesheet[1])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Attack(pygame.sprite.Sprite):
    """
    Represents an attack in the game.

    Attributes:
        game (Game): The game instance.
        x (int): The x-coordinate of the attack.
        y (int): The y-coordinate of the attack.
        width (int): The width of the attack.
        height (int): The height of the attack.
        direction (str): The direction the attack is facing.
        animation_loop (float): The current animation frame of the attack.
        damage (int): The damage inflicted by the attack.
        dx (float): The horizontal movement speed of the attack.
        dy (float): The vertical movement speed of the attack.
        image (Surface): The image of the attack.
        rect (Rect): The rectangular area occupied by the attack.
        animations (list): The list of animation frames for the attack.

    Methods:
        __init__(self, game, x, y): Initializes a new instance of the Attack class.
        update(self): Updates the attack.
        collide(self): Handles collision with enemies.
        animate(self): Animates the attack.
        movement(self): Moves the attack.
        upgrade_attack_tier(self, tier): Upgrades the attack to a higher tier.
    """

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

        self.damage = (
            self.game.player.basic_attack_damage
            + 3 * self.game.player.basic_attack_level
        )
        mouse_position = pygame.mouse.get_pos()

        # Calculate the angle between the player and the mouse
        # The angle is used to determine the direction of the attack
        # and the speed of the attack
        # The attack moves towards the mouse
        # The attack moves faster if the mouse is further away
        # The attack moves slower if the mouse is closer

        angle = math.atan2(mouse_position[1] - self.y, mouse_position[0] - self.x)
        # Calculate the horizontal movement speed of the attack
        self.dx = math.cos(angle) * self.game.player.player_speed
        # Calculate the vertical movement speed of the attack
        self.dy = math.sin(angle) * self.game.player.player_speed

        self.image = self.game.attack_spritesheet.get_sprite(
            0, 0, self.width, self.height, BLACK
        )

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # Base attack animations
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
        if self.__class__.__name__ == "Attack":
            self.upgrade_attack_tier(self.game.player.basic_attack_level // 3)

    def update(self):

        self.collide()
        self.movement()
        self.animate()

    def collide(self):
        # Check for collisions with enemies
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            # If the player's basic attack level is less than 3
            if self.game.player.basic_attack_level < 3:
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
                    # If the player's basic attack level is between 3 and 6
            elif (
                self.game.player.basic_attack_level >= 3
                and self.game.player.basic_attack_level < 6
            ):
                for sprite in hits:
                    sprite.health -= self.damage * 2
                    self.kill()
                    Temporary_text_damage(
                        self.game,
                        self.damage * 2,
                        "red",
                        sprite.rect.x,
                        sprite.rect.y + 32,
                        pygame.font.Font(
                            "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                        ),
                    )
                    # If the player's basic attack level is between 6 and 9
            elif (
                self.game.player.basic_attack_level >= 6
                and self.game.player.basic_attack_level < 9
            ):
                for sprite in hits:
                    sprite.health -= self.damage * 2
                    sprite.speed -= 0.05
                    self.kill()
                    Temporary_text_damage(
                        self.game,
                        self.damage * 2,
                        "red",
                        sprite.rect.x,
                        sprite.rect.y + 32,
                        pygame.font.Font(
                            "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                        ),
                    )
                    # If the player's basic attack level is between 9 and 12
            elif (
                self.game.player.basic_attack_level >= 9
                and self.game.player.basic_attack_level < 12
            ):
                for sprite in hits:
                    sprite.health -= self.damage * 3
                    sprite.speed -= 0.1
                    self.kill()
                    Temporary_text_damage(
                        self.game,
                        self.damage * 3,
                        "red",
                        sprite.rect.x,
                        sprite.rect.y + 32,
                        pygame.font.Font(
                            "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                        ),
                    )
                    # If the player's basic attack level is between 12 and 15
            elif (
                self.game.player.basic_attack_level >= 12
                and self.game.player.basic_attack_level < 15
            ):
                for sprite in hits:
                    sprite.health -= self.damage * 4
                    self.kill()
                    Temporary_text_damage(
                        self.game,
                        self.damage * 3,
                        "red",
                        sprite.rect.x,
                        sprite.rect.y + 32,
                        pygame.font.Font(
                            "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                        ),
                    )
                    # If the player's basic attack level is greater than 15
            else:
                for sprite in hits:
                    sprite.health -= self.damage * 5
                    sprite.speed -= 0.25
                    self.kill()
                    Temporary_text_damage(
                        self.game,
                        self.damage * 3,
                        "red",
                        sprite.rect.x,
                        sprite.rect.y + 32,
                        pygame.font.Font(
                            "font/pixel_font.ttf", 12 + int(self.damage * 0.5)
                        ),
                    )
            for sprite in hits:
                if sprite.name[-5:] == "Mouse":
                    self.game.music.play_sound("mouse_sound")
                elif sprite.name[:6] == "Desert":
                    if sprite.name[-4:] != "Boss":
                        self.game.music.play_sound("desert_sound")
                    else:
                        self.game.music.play_sound("desert_boss_sound")
                elif sprite.name[:5] == "Burnt":
                    if sprite.name[-8:] == "Succubus":
                        self.game.music.play_sound("succubus_sound")
                    elif sprite.name[-5:] == "Angel":
                        self.game.music.play_sound("fallen_angel_sound")
                    else:
                        self.game.music.play_sound("burnt_sound")
                elif sprite.name == "Dragon":
                    self.game.music.play_sound("dragon_sound")

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= len(self.animations):
            self.kill()

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)

    def upgrade_attack_tier(self, tier):
        # Upgrade the attack to a higher tier based on the player's basic attack level and speed level (speed level affects the number of attack animations) and
        # the tier of the attack (tier 1, 2, 3, or 4)
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
        if tier == 3:
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
        elif tier >= 4:
            attack_spritesheet = Spritesheet("images/missles/icetacle.png")
            self.animations = [
                attack_spritesheet.get_sprite(
                    0, 0, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    128, 0, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    256, 0, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    384, 0, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    0, 128, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    128, 128, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    256, 128, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    384, 128, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    0, 256, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    128, 256, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    256, 256, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    384, 256, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    0, 384, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    128, 384, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    256, 384, self.width * 2, self.height * 2, BLACK
                ),
                attack_spritesheet.get_sprite(
                    384, 384, self.width * 2, self.height * 2, BLACK
                ),
            ] * (self.game.player.speed_level + 1)
            self.image = pygame.transform.scale(
                self.image, (TILESIZE * 2, TILESIZE * 2)
            )


class Ultimate_attack(Attack):
    """
    Represents the ultimate attack in the game.

    Inherits from the Attack class.

    Attributes:
    - game (Game): The game instance.
    - x (int): The x-coordinate of the ultimate attack.
    - y (int): The y-coordinate of the ultimate attack.
    - width (int): The width of the ultimate attack.
    - height (int): The height of the ultimate attack.
    - animations (list): List of animation frames for the ultimate attack.
    - image (Surface): The current image of the ultimate attack.
    - damage (int): The damage caused by the ultimate attack.
    - rect (Rect): The rectangular area occupied by the ultimate attack.
    - count (int): The count of how many times the ultimate attack has hit an enemy.

    Methods:
    - __init__(self, game, x, y): Initializes the Ultimate_attack instance.
    - upgrade_attack_tier(self, tier): Upgrades the attack tier of the ultimate attack.
    - collide(self): Handles collision detection and damage calculation for the ultimate attack.
    - animate(self): Animates the ultimate attack by updating the current image.
    """

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
        ] * (self.game.player.speed_level + 1)
        # Upgrade the ultimate attack based on the player's ultimate attack level
        self.upgrade_attack_tier(self.game.player.ultimate_attack_level // 3)
        self.image = self.animations[0]
        self.damage = (
            self.game.player.ultimate_attack_damage
            + self.game.player.ultimate_attack_level * 5
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.count = 0

    def upgrade_attack_tier(self, tier):

        if tier == 1:
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (256, 256)
                )
            self.height *= 2
            self.width *= 2

        elif tier == 2:
            # Upgrade the ultimate attack to tier 2
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
            ] * (self.game.player.speed_level + 1)
            # Scale the ultimate attack to a larger size
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
            ] * (self.game.player.speed_level + 1)
            self.height *= 4
            self.width *= 4
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (512, 512)
                )

    def collide(self):
        self.max_count = 1 + 1 * self.game.player.ultimate_attack_level

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for sprite in hits:
                sprite.health -= self.damage
                self.count += 1
                if self.count >= self.max_count:
                    self.kill()
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
            for sprite in hits:
                if sprite.name[-5:] == "Mouse":
                    self.game.music.play_sound("mouse_sound")
                elif sprite.name[:6] == "Desert":
                    if sprite.name[-4:] != "Boss":
                        self.game.music.play_sound("desert_sound")
                    else:
                        self.game.music.play_sound("desert_boss_sound")
                elif sprite.name[:5] == "Burnt":
                    if sprite.name[-8:] == "Succubus":
                        self.game.music.play_sound("succubus_sound")
                    elif sprite.name[-5:] == "Angel":
                        self.game.music.play_sound("fallen_angel_sound")
                    else:
                        self.game.music.play_sound("burnt_sound")
                elif sprite.name == "Dragon":
                    self.game.music.play_sound("dragon_sound")

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
        self.direction = self.enemy.facing
        self.damage = self.enemy.damage
        # Calculate the angle between the player and the enemy
        self.angle = math.atan2(
            self.game.player.rect.y - self.y, self.game.player.rect.x - self.x
        )

        self.dx = math.cos(self.angle) * self.enemy.speed * 2
        self.dy = math.sin(self.angle) * self.enemy.speed * 2

        self.spritesheet = self.enemy.enemy_attack_spritesheet
        self.animation_speed = 0.15
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
            self.animations = [self.image] * 35

        elif name == "Brown Mouse":
            self.image = self.spritesheet.get_sprite(0, 0, 16, 8, WHITE)
            self.image = pygame.transform.scale(self.image, (32, 16))
            self.animations = [
                pygame.transform.rotate(self.image, i * 15) for i in range(24)
            ]
        elif name == "White Mouse":
            self.image = self.spritesheet.get_sprite(0, 0, 55, 5, WHITE)
            self.image = pygame.transform.scale(self.image, (64, 8))

            self.image = pygame.transform.rotate(
                self.image, 180 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 35
        elif name == "Boss Mouse":
            self.image = self.spritesheet.get_sprite(0, 0, 44, 30, WHITE)
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(
                self.image, 290 - math.degrees(self.angle)
            )

            self.animations = [self.image] * 30
        elif name == "Desert Boarman":
            self.image = self.spritesheet.get_sprite(0, 0, 24, 22, WHITE)
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(
                self.image, 180 - math.degrees(self.angle)
            )
            self.animation_speed = 1
            self.animations = [
                pygame.transform.rotate(self.image, i * 5) for i in range(60)
            ]
        elif name == "Desert Wolf":
            self.image = self.spritesheet.get_sprite(0, 0, 85, 5, WHITE)
            self.image = pygame.transform.scale(self.image, (96, 8))
            self.image = pygame.transform.rotate(
                self.image, 180 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 30
        elif name == "Desert Wartotaur":
            self.image = self.spritesheet.get_sprite(0, 0, 60, 47, WHITE)
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.image = pygame.transform.rotate(
                self.image, 240 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 30
        elif name == "Desert Boss":
            self.image = self.enemy.enemy_attack_spritesheet.get_sprite(
                0, 0, 64, 64, WHITE
            )
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.animation_speed = 1.25
            self.animations = [
                self.enemy.enemy_attack_spritesheet.get_sprite(0, 0, 64, 64, WHITE),
                self.enemy.enemy_attack_spritesheet.get_sprite(0, 64, 64, 64, WHITE),
                self.enemy.enemy_attack_spritesheet.get_sprite(0, 128, 64, 64, WHITE),
                self.enemy.enemy_attack_spritesheet.get_sprite(0, 192, 64, 64, WHITE),
            ] * 20
        elif name == "Burnt Imp":
            self.image = self.spritesheet.get_sprite(0, 0, 95, 19, WHITE)
            self.image = pygame.transform.scale(self.image, (96, 16))
            self.image = pygame.transform.rotate(
                self.image, 180 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 30
        elif name == "Burnt Succubus":
            self.image = self.spritesheet.get_sprite(0, 0, 93, 13, WHITE)
            self.image = pygame.transform.scale(self.image, (96, 16))
            self.image = pygame.transform.rotate(
                self.image, 180 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 30
        elif name == "Burnt Fallen Angel":
            self.image = self.spritesheet.get_sprite(0, 11, 11, 11, WHITE)
            self.animations = [
                self.spritesheet.get_sprite(0, 11, 11, 11, WHITE),
                self.spritesheet.get_sprite(16, 7, 18, 18, WHITE),
                self.spritesheet.get_sprite(46, 4, 22, 22, WHITE),
                self.spritesheet.get_sprite(76, 1, 28, 28, WHITE),
                self.spritesheet.get_sprite(106, 0, 31, 31, WHITE),
            ] * 6
        elif name == "Dragon":
            self.image = self.spritesheet.get_sprite(0, 0, 17, 10, WHITE)
            self.animations = [
                self.spritesheet.get_sprite(0, 0, 17, 10, WHITE),
                self.spritesheet.get_sprite(18, 0, 18, 10, WHITE),
                self.spritesheet.get_sprite(16, 0, 16, 10, WHITE),
            ] * 10
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (64, 32)
                )
                self.animations[i] = pygame.transform.rotate(
                    self.animations[i], 180 - math.degrees(self.angle)
                )

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        if hits:
            for sprite in hits:
                if sprite.__class__.__name__ == "Player":
                    self.game.music.play_sound("player_hurt")
                    self.game.health_bar.lose(self.damage)
                    self.kill()

    def update(self):
        self.collide()
        self.movement()
        self.animate()

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += self.animation_speed + (self.enemy.speed * 0.05)
        if self.animation_loop >= len(self.animations):
            self.kill()

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx) * 2
        self.rect.y = self.rect.y + int(self.dy) * 2


class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy entity in the game.

    Attributes:
        game (Game): The game instance.
        x (int): The x-coordinate of the enemy's position.
        y (int): The y-coordinate of the enemy's position.
        enemy_spritesheet_path (str): The file path to the enemy's spritesheet.
        enemy_attack_spritesheet_path (str): The file path to the enemy's attack spritesheet.
        name (str): The name of the enemy.
        damage (int): The amount of damage the enemy can inflict.
        health (int): The current health of the enemy.
        exp (int): The amount of experience points the enemy gives when defeated.
        speed (int): The movement speed of the enemy.
        respawn_id (Optional[int]): The ID of the enemy's respawn point (if applicable).
    """

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
        respawn_id=None,
    ):

        self.enemy_spritesheet_path = enemy_spritesheet_path
        self.enemy_attack_spritesheet_path = enemy_attack_spritesheet_path
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.height, self.width = TILESIZE, TILESIZE

        self.facing = random.choice(["up", "down", "right", "left"])
        self.animation_loop = 0
        self.enemy_spritesheet = Spritesheet(enemy_spritesheet_path)
        self.enemy_attack_spritesheet = Spritesheet(enemy_attack_spritesheet_path)
        self.dist = 1000
        self.image = self.enemy_spritesheet.get_sprite(
            1, 128, self.width, self.height, WHITE
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.respawn_id = respawn_id
        self.animate_speed = 0.15
        self.speed = speed
        self.name = name
        self.damage = damage
        self.health = health
        self.experience = exp
        self.shoot_cooldown_count = 0
        self.up_animations = [
            self.enemy_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(64, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(128, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(192, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(256, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(320, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(384, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(448, 0, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(512, 0, self.width, self.height, WHITE),
        ]

        self.down_animations = [
            self.enemy_spritesheet.get_sprite(0, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(64, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(128, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(192, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(256, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(320, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(384, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(448, 128, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(512, 128, self.width, self.height, WHITE),
        ]

        self.right_animations = [
            self.enemy_spritesheet.get_sprite(0, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(64, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(128, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(192, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(256, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(320, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(384, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(448, 192, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(512, 192, self.width, self.height, WHITE),
        ]

        self.left_animations = [
            self.enemy_spritesheet.get_sprite(0, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(64, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(128, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(192, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(256, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(320, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(384, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(448, 64, self.width, self.height, WHITE),
            self.enemy_spritesheet.get_sprite(512, 64, self.width, self.height, WHITE),
        ]
        self.personalize(self.name)
        self.attack = self.enemy_attack_spritesheet.get_sprite(0, 0, 64, 32, BLACK)

    def personalize(self, name):
        # Personalize the enemy based on its name
        if name == "Grey Mouse":
            self.max_cooldown_count = 175
        elif name == "Brown Mouse":
            self.max_cooldown_count = 100
        elif name == "White Mouse":
            self.max_cooldown_count = 80
        elif name == "Desert Boarman":
            self.max_cooldown_count = 80
        elif name == "Desert Wolf":
            self.max_cooldown_count = 60
            self.image = self.enemy_spritesheet.get_sprite(
                0, 0, self.width * 2, self.height, WHITE
            )

            self.up_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 0, self.width * 2, self.height, WHITE
                ),
            ]

            self.down_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 140, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 140, self.width * 2, self.height, WHITE
                ),
            ]

            self.right_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 223, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 223, self.width * 2, self.height, WHITE
                ),
            ]

            self.left_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 64, self.width * 2, self.height, WHITE
                ),
            ]
        elif name == "Desert Wartotaur":
            self.max_cooldown_count = 80
        elif (
            name == "Burnt Imp"
            or name == "Burnt Succubus"
            or name == "Burnt Fallen Angel"
        ):
            self.max_cooldown_count = 60
            self.image = self.enemy_spritesheet.get_sprite(
                0, 0, self.width * 2, self.height, WHITE
            )
            self.up_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 0, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 0, self.width * 2, self.height, WHITE
                ),
            ]

            self.down_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 128, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 128, self.width * 2, self.height, WHITE
                ),
            ]

            self.right_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 192, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 192, self.width * 2, self.height, WHITE
                ),
            ]

            self.left_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    640, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    768, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    896, 64, self.width * 2, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    1024, 64, self.width * 2, self.height, WHITE
                ),
            ]

        elif name == "Burnt Fallen Angel":
            self.max_cooldown_count = 25

    def update(self):
        # Update the enemy's position, animation, and attack cooldown
        # based on the player's position
        # and the enemy's name
        # If the enemy is a Mouse... and the player is in the first area

        if (
            self.name[-5:] == "Mouse"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 > -37
        ):

            self.cooldown()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
        # If the enemy is a Desert... and the player is in the second area
        elif (
            self.name[:6] == "Desert"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 < -36
        ):

            self.cooldown()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
        # If the enemy is a Burnt... and the player is in the third area
        elif (
            self.name[:5] == "Burnt"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 < -54
        ):

            self.cooldown()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()

    def collide(self, direction):
        if self.dist < 600:
            if direction == "x":
                hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
                if hits:
                    if self.facing == "right":
                        self.rect.x = hits[0].rect.left - self.rect.width
                    if self.facing == "left":
                        self.rect.x = hits[0].rect.right

            if direction == "y":
                hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
                if hits:
                    if self.facing == "up":
                        self.rect.y = hits[0].rect.bottom
                    if self.facing == "down":
                        self.rect.y = hits[0].rect.top - self.rect.height

    def attack_player(self):
        # Attack the player if the enemy is within range
        if self.dist < 600:
            self.shoot_cooldown_count += 1
            if self.facing == "up":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "down":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "left":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "right":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)

    def movement(self):
        self.dist = math.hypot(
            self.game.player.rect.x - self.rect.x,
            self.game.player.rect.y - self.rect.y,
        )

        if self.dist < 600:
            if self.game.player.rect.x > self.rect.x:

                self.rect.x += self.speed
                self.facing = "right"

            elif self.game.player.rect.x < self.rect.x:

                self.rect.x -= self.speed
                self.facing = "left"

            elif self.game.player.rect.y > self.rect.y:

                self.rect.y += self.speed
                self.facing = "down"

            elif self.game.player.rect.y < self.rect.y:

                self.rect.y -= self.speed
                self.facing = "up"

    def animate(self):
        if self.dist < 600:
            if self.facing == "down":

                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

            if self.facing == "up":

                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

            if self.facing == "left":

                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

            if self.facing == "right":

                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.right_animations):
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
        # Check if the enemy's health is less than or equal to 0
        # and shows the experience gained
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

            self.game.spawner.add(self.respawn_id)
            if self.name == "Dragon":
                self.game.active_game = 0
                self.game.win = 1
                self.game.end_screen()

    def cooldown(self):
        if self.shoot_cooldown_count >= self.max_cooldown_count:
            self.shoot_cooldown_count = 0
        elif self.shoot_cooldown_count > 0:
            self.shoot_cooldown_count += 1


class Boss(Enemy):
    def __init__(
        self,
        game,
        x,
        y,
        enemy_spritesheet_path,
        enemy_attack_spritesheet_path,
        boss_attack_spritesheet_path,
        name,
        damage,
        health,
        exp,
        speed,
        respawn_id=None,
    ):
        super().__init__(
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
            respawn_id=respawn_id,
        )
        self.boss_attack_spritesheet = Spritesheet(boss_attack_spritesheet_path)
        self.max_cooldown_count = 75
        self.ultimate_cooldown_count = 0
        self.ultimate_cooldown_max = 100
        self.personalize(self.name)

    def update(self):
        if (
            self.name[-5:] == "Mouse"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 > -37
        ):
            self.cooldown()
            self.cooldown_ultimate()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
            if self.ultimate_cooldown_count == 0:
                self.ultimate_attack_player()
        elif (
            self.name[:6] == "Desert"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 > -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 < -36
        ):

            self.cooldown()
            self.cooldown_ultimate()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
            if self.ultimate_cooldown_count == 0:
                self.ultimate_attack_player()
        elif (
            self.name[:5] == "Burnt"
            and self.game.player.absolute_sprite_moved_value[0] / 69268 // 16 < -80
            and self.game.player.absolute_sprite_moved_value[1] / 69268 // 16 < -55
        ):
            self.cooldown()
            self.cooldown_ultimate()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
            if self.ultimate_cooldown_count == 0:
                self.ultimate_attack_player()
        elif self.name == "Dragon":
            self.cooldown()
            self.cooldown_ultimate()
            self.collide("x")
            self.movement()
            self.collide("y")
            self.animate()

            self.check_health()
            if self.shoot_cooldown_count == 0:
                self.attack_player()
            if self.ultimate_cooldown_count == 0:
                self.ultimate_attack_player()

    def ultimate_attack_player(self):
        self.ultimate_cooldown_count += 1
        if self.dist < 850:
            Boss_attack(self.game, self.rect.x, self.rect.y, self)

    def personalize(self, name):
        if name == "Boss Mouse":
            self.max_cooldown_count = 50

        elif name == "Desert Boss":
            self.max_cooldown_count = 25
            self.ultimate_cooldown_max = 200

            self.up_animations = [
                self.enemy_spritesheet.get_sprite(0, 0, self.width, self.height, WHITE),
                self.enemy_spritesheet.get_sprite(
                    64, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    192, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    320, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    448, 0, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 0, self.width, self.height, WHITE
                ),
            ]

            self.down_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    64, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    192, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    320, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    448, 128, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 128, self.width, self.height, WHITE
                ),
            ]

            self.right_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    64, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    192, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    320, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    448, 192, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 192, self.width, self.height, WHITE
                ),
            ]

            self.left_animations = [
                self.enemy_spritesheet.get_sprite(
                    0, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    64, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    128, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    192, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    256, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    320, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    384, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    448, 64, self.width, self.height, WHITE
                ),
                self.enemy_spritesheet.get_sprite(
                    512, 64, self.width, self.height, WHITE
                ),
            ]

            for i in range(9):
                self.left_animations[i] = pygame.transform.scale(
                    self.left_animations[i], (128, 128)
                )
                self.right_animations[i] = pygame.transform.scale(
                    self.right_animations[i], (128, 128)
                )
                self.up_animations[i] = pygame.transform.scale(
                    self.up_animations[i], (128, 128)
                )
                self.down_animations[i] = pygame.transform.scale(
                    self.down_animations[i], (128, 128)
                )
        elif name == "Dragon":
            self.max_cooldown_count = 40
            self.ultimate_cooldown_max = 350
            self.animate_speed = 0.05
            self.up_animations = [
                self.enemy_spritesheet.get_sprite(0, 0, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(144, 0, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(288, 0, 144, 128, BLACK),
            ]
            self.right_animations = [
                self.enemy_spritesheet.get_sprite(0, 128, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(144, 128, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(288, 128, 144, 128, BLACK),
            ]
            self.down_animations = [
                self.enemy_spritesheet.get_sprite(0, 256, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(144, 256, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(288, 256, 144, 128, BLACK),
            ]
            self.left_animations = [
                self.enemy_spritesheet.get_sprite(0, 384, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(144, 384, 144, 128, BLACK),
                self.enemy_spritesheet.get_sprite(288, 384, 144, 128, BLACK),
            ]
            for i in range(3):
                self.left_animations[i] = pygame.transform.scale(
                    self.left_animations[i], (288, 256)
                )
                self.right_animations[i] = pygame.transform.scale(
                    self.right_animations[i], (288, 256)
                )
                self.up_animations[i] = pygame.transform.scale(
                    self.up_animations[i], (288, 256)
                )
                self.down_animations[i] = pygame.transform.scale(
                    self.down_animations[i], (288, 256)
                )

    def cooldown_ultimate(self):

        if self.ultimate_cooldown_count >= self.ultimate_cooldown_max:
            self.ultimate_cooldown_count = 0
        elif self.ultimate_cooldown_count > 0:
            self.ultimate_cooldown_count += 1


class Boss_attack(Enemy_attack):
    def __init__(self, game, x, y, enemy):
        super().__init__(game, x, y, enemy)
        self.damage = self.enemy.damage * 3
        self.personalize(self.enemy.name)

    def personalize(self, name):
        if name == "Boss Mouse":

            self.image = self.enemy.boss_attack_spritesheet.get_sprite(
                0, 0, 44, 30, WHITE
            )
            self.image = pygame.transform.scale(self.image, (128, 64))
            self.image = pygame.transform.rotate(
                self.image, 290 - math.degrees(self.angle)
            )
            self.animations = [self.image] * 35
        elif name == "Desert Boss":
            self.image = self.enemy.boss_attack_spritesheet.get_sprite(
                0, 0, 45, 23, WHITE
            )
            self.image = pygame.transform.scale(self.image, (128, 64))
            self.animation_speed = 1
            self.animations = [
                pygame.transform.rotate(self.image, i * 5) for i in range(60)
            ]
            self.damage = self.enemy.damage * 5
            self.image = self.enemy.boss_attack_spritesheet.get_sprite(
                0, 0, 64, 64, WHITE
            )
        elif name == "Dragon":
            self.image = self.enemy.boss_attack_spritesheet.get_sprite(
                0, 0, 32, 32, BLACK
            )
            self.animations = [
                self.enemy.boss_attack_spritesheet.get_sprite(0, 0, 32, 32, BLACK),
                self.enemy.boss_attack_spritesheet.get_sprite(32, 0, 32, 32, BLACK),
                self.enemy.boss_attack_spritesheet.get_sprite(64, 0, 32, 32, BLACK),
                self.enemy.boss_attack_spritesheet.get_sprite(96, 0, 32, 32, BLACK),
            ] * 5
            self.damage = self.enemy.damage * 10
            for i in range(len(self.animations)):
                self.animations[i] = pygame.transform.rotate(
                    self.animations[i], 90 - math.degrees(self.angle)
                )
                self.animations[i] = pygame.transform.scale(
                    self.animations[i], (128, 128)
                )

    def movement(self):
        self.rect.x = self.rect.x + int(self.dx) * 2.5
        self.rect.y = self.rect.y + int(self.dy) * 2.5


class Last_boss(Boss):
    def __init__(
        self,
        game,
        x,
        y,
        enemy_spritesheet_path,
        enemy_attack_spritesheet_path,
        boss_attack_spritesheet_path,
        name,
        damage,
        health,
        exp,
        speed,
        respawn_id=None,
    ):
        super().__init__(
            game,
            x,
            y,
            enemy_spritesheet_path,
            enemy_attack_spritesheet_path,
            boss_attack_spritesheet_path,
            name,
            damage,
            health,
            exp,
            speed,
            respawn_id,
        )

    def attack_player(self):

        if self.dist < 1200:
            self.shoot_cooldown_count += 1
            if self.facing == "up":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "down":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "left":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)
            if self.facing == "right":
                Enemy_attack(self.game, self.rect.x, self.rect.y, self)

    def movement(self):
        self.dist = math.hypot(
            self.game.player.rect.x - self.rect.x,
            self.game.player.rect.y - self.rect.y,
        )

        if self.dist < 1200:
            if self.game.player.rect.x > self.rect.x:

                self.rect.x += self.speed
                self.facing = "right"

            elif self.game.player.rect.x < self.rect.x:

                self.rect.x -= self.speed
                self.facing = "left"

            elif self.game.player.rect.y > self.rect.y:

                self.rect.y += self.speed
                self.facing = "down"

            elif self.game.player.rect.y < self.rect.y:

                self.rect.y -= self.speed
                self.facing = "up"

    def animate(self):
        if self.dist < 1200:
            if self.facing == "down":

                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

            if self.facing == "up":

                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

            if self.facing == "left":

                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

            if self.facing == "right":

                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animate_speed
                if self.animation_loop >= len(self.right_animations):
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
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.game.music.play_sound("player_death")
            self.game.active_game = 0


class Exp_bar(Bar):
    def __init__(self, game, x, y, w, h, full, bg, fg):
        super().__init__(game, x, y, w, h, full, bg, fg)
        self.remaining = 0

    def lose(self):
        self.full = self.full + int((self.game.player.level // 0.8) ** 2)

    def get(self, amount):
        if self.remaining < self.full:
            self.remaining += amount
        if self.remaining >= self.full:
            self.game.paused_game = 1
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


class Music:
    def __init__(self):
        self.music = {
            "main_menu": "sounds/Music/main_menu_music.ogg",
            "level_1": "sounds/Music/level1_music.wav",
            "level_2": "sounds/Music/level2_music.mp3",
            "level_3": "sounds/Music/level3_music.mp3",
            "boss_room": "sounds/Music/boss_room_music.flac",
            "victory" : "sounds/Music/victory_music.mp3",
        }
        self.sound = {
            "button_click": pygame.mixer.Sound("sounds/Sound/button_sound.flac"),
            "level_up": pygame.mixer.Sound("sounds/Sound/level_up_sound.mp3"),
            "mouse_sound": pygame.mixer.Sound("sounds/Sound/mouse_sound.mp3"),
            "desert_sound": pygame.mixer.Sound("sounds/Sound/desert_sound.mp3"),
            "desert_boss_sound": pygame.mixer.Sound(
                "sounds/Sound/desert_boss_sound.mp3"
            ),
            "burnt_sound": pygame.mixer.Sound("sounds/Sound/burnt_sound.mp3"),
            "succubus_sound": pygame.mixer.Sound("sounds/Sound/succubus_sound.mp3"),
            "fallen_angel_sound": pygame.mixer.Sound(
                "sounds/Sound/fallen_angel_sound.mp3"
            ),
            "player_hurt": pygame.mixer.Sound("sounds/Sound/player_hurt_sound.mp3"),
            "player_death": pygame.mixer.Sound("sounds/Sound/player_death_sound.mp3"),
            "dragon_sound": pygame.mixer.Sound("sounds/Sound/dragon_sound.mp3"),
            "game_over": pygame.mixer.Sound("sounds/Sound/game_over_sound.mp3"),
        }

    def play_music(self, name):
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.play(-1)

    def play_sound(self, name):
        self.sound[name].play()
        if name == "level_up":
            self.sound[name].set_volume(0.25)
        elif name == "player_hurt":
            self.sound[name].set_volume(0.08)
        elif name == "player_death":
            self.sound[name].set_volume(0.5)
        elif name == "game_over":
            self.sound[name].set_volume(0.4)
        elif name == "mouse_sound":
            self.sound[name].set_volume(0.15)
        elif name == "desert_sound":
            self.sound[name].set_volume(0.15)
        elif name == "desert_boss_sound":
            self.sound[name].set_volume(0.25)
        elif name == "burnt_sound":
            self.sound[name].set_volume(0.15)
        elif name == "succubus_sound":
            self.sound[name].set_volume(0.1)
        elif name == "fallen_angel_sound":
            self.sound[name].set_volume(0.4)
        elif name == "dragon_sound":
            self.sound[name].set_volume(0.2)


class Spawner:
    def __init__(self, game):

        self.game = game
        self.respawn_time = ENEMIES_RESPAWN_TIME

        self.current = self.respawn_time
        self.hashmap_of_enemies = {
            "Grey Mouse": [],
            "Brown Mouse": [],
            "White Mouse": [],
            "Boss Mouse": [],
            "Desert Boarman": [],
            "Desert Wolf": [],
            "Desert Wartotaur": [],
            "Desert Boss": [],
            "Burnt Imp": [],
            "Burnt Succubus": [],
            "Burnt Fallen Angel": [],
            "Dragon": [],
        }

        self.list_of_dead_enemies = []
        self.list_of_all_enemies = [enemy for enemy in self.game.enemies.sprites()]
        for i in range(len(self.list_of_all_enemies)):
            if self.list_of_all_enemies[i].name == "Grey Mouse":
                self.hashmap_of_enemies["Grey Mouse"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "e",
                    len(self.hashmap_of_enemies["Grey Mouse"]),
                )
            elif self.list_of_all_enemies[i].name == "Brown Mouse":
                self.hashmap_of_enemies["Brown Mouse"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "a",
                    len(self.hashmap_of_enemies["Brown Mouse"]),
                )
            elif self.list_of_all_enemies[i].name == "White Mouse":
                self.hashmap_of_enemies["White Mouse"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "s",
                    len(self.hashmap_of_enemies["White Mouse"]),
                )
            elif self.list_of_all_enemies[i].name == "Boss Mouse":
                self.hashmap_of_enemies["Boss Mouse"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "m",
                    len(self.hashmap_of_enemies["Boss Mouse"]),
                )
            elif self.list_of_all_enemies[i].name == "Desert Boarman":
                self.hashmap_of_enemies["Desert Boarman"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "b",
                    len(self.hashmap_of_enemies["Desert Boarman"]),
                )
            elif self.list_of_all_enemies[i].name == "Desert Wolf":
                self.hashmap_of_enemies["Desert Wolf"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "w",
                    len(self.hashmap_of_enemies["Desert Wolf"]),
                )
            elif self.list_of_all_enemies[i].name == "Desert Wartotaur":
                self.hashmap_of_enemies["Desert Wartotaur"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "W",
                    len(self.hashmap_of_enemies["Desert Wartotaur"]),
                )
            elif self.list_of_all_enemies[i].name == "Desert Boss":
                self.hashmap_of_enemies["Desert Boss"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "M",
                    len(self.hashmap_of_enemies["Desert Boss"]),
                )
            elif self.list_of_all_enemies[i].name == "Burnt Imp":
                self.hashmap_of_enemies["Burnt Imp"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "i",
                    len(self.hashmap_of_enemies["Burnt Imp"]),
                )
            elif self.list_of_all_enemies[i].name == "Burnt Succubus":
                self.hashmap_of_enemies["Burnt Succubus"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "u",
                    len(self.hashmap_of_enemies["Burnt Succubus"]),
                )
            elif self.list_of_all_enemies[i].name == "Burnt Fallen Angel":
                self.hashmap_of_enemies["Burnt Fallen Angel"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "f",
                    len(self.hashmap_of_enemies["Burnt Fallen Angel"]),
                )
            elif self.list_of_all_enemies[i].name == "Dragon":
                self.hashmap_of_enemies["Dragon"].append(
                    [
                        self.list_of_all_enemies[i].rect.x // 64,
                        self.list_of_all_enemies[i].rect.y // 64,
                    ]
                )
                self.list_of_all_enemies[i].respawn_id = (
                    "d",
                    len(self.hashmap_of_enemies["Dragon"]),
                )

    def add(self, respawn_id):
        self.list_of_dead_enemies.append(respawn_id)

    def update(self):

        if self.current == 0:

            if self.list_of_dead_enemies:

                for i in range(len(self.list_of_dead_enemies)):

                    for j in range(len(self.list_of_all_enemies)):

                        if (
                            self.list_of_dead_enemies[i][0]
                            == self.list_of_all_enemies[j].respawn_id[0]
                            and self.list_of_dead_enemies[i][1]
                            == self.list_of_all_enemies[j].respawn_id[1]
                        ):

                            if self.list_of_dead_enemies[i][0] == "e":

                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Grey Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Grey Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_1/grey_mouse_child.png",
                                    "images/enemies/level_1/grey_mouse_child_attack.png",
                                    "Grey Mouse",
                                    2,
                                    10,
                                    2,
                                    1.35,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "a":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Brown Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Brown Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_1/brown_mouse_assassin.png",
                                    "images/enemies/level_1/brown_mouse_assassin_attack.png",
                                    "Brown Mouse",
                                    6,
                                    20,
                                    5,
                                    2,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "s":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["White Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["White Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_1/white_mouse_spearman.png",
                                    "images/enemies/level_1/white_mouse_spearman_attack.png",
                                    "White Mouse",
                                    15,
                                    30,
                                    10,
                                    2.25,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "m":
                                Boss(
                                    self.game,
                                    self.hashmap_of_enemies["Boss Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Boss Mouse"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_1/mouse_boss.png",
                                    "images/enemies/level_1/mouse_boss_attack.png",
                                    "images/enemies/level_1/mouse_boss_boss_attack.png",
                                    "Boss Mouse",
                                    25,
                                    200,
                                    100,
                                    2.5,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "b":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Desert Boarman"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Desert Boarman"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_2/desert_boarman.png",
                                    "images/enemies/level_2/desert_boarman_attack.png",
                                    "Desert Boarman",
                                    25,
                                    225,
                                    75,
                                    2.25,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "w":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Desert Wolf"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Desert Wolf"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_2/desert_wolf.png",
                                    "images/enemies/level_2/desert_wolf_attack.png",
                                    "Desert Wolf",
                                    35,
                                    250,
                                    100,
                                    2.75,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "W":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Desert Wartotaur"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Desert Wartotaur"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_2/desert_wartotaur.png",
                                    "images/enemies/level_2/desert_wartotaur_attack.png",
                                    "Desert Wartotaur",
                                    55,
                                    500,
                                    250,
                                    2.5,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "M":
                                Boss(
                                    self.game,
                                    self.hashmap_of_enemies["Desert Boss"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Desert Boss"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_2/desert_minotaur_boss.png",
                                    "images/enemies/level_2/skull.png",
                                    "images/enemies/level_2/desert_minotaur_boss_attack.png",
                                    "Desert Boss",
                                    40,
                                    2500,
                                    1000,
                                    3.0,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "i":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Burnt Imp"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Burnt Imp"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_3/burnt_imp.png",
                                    "images/enemies/level_3/burnt_imp_attack.png",
                                    "Burnt Imp",
                                    75,
                                    750,
                                    375,
                                    3.0,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "u":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Burnt Succubus"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Burnt Succubus"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_3/burnt_succubus.png",
                                    "images/enemies/level_3/burnt_succubus_attack.png",
                                    "Burnt Succubus",
                                    100,
                                    1500,
                                    750,
                                    3.25,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )
                            elif self.list_of_dead_enemies[i][0] == "f":
                                Enemy(
                                    self.game,
                                    self.hashmap_of_enemies["Burnt Fallen Angel"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][0]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[0]
                                        / 69268
                                        // 16
                                    ),
                                    self.hashmap_of_enemies["Burnt Fallen Angel"][
                                        self.list_of_all_enemies[j].respawn_id[1] - 1
                                    ][1]
                                    + (
                                        self.game.player.absolute_sprite_moved_value[1]
                                        / 69268
                                        // 16
                                    ),
                                    "images/enemies/level_3/burnt_fallen_angel.png",
                                    "images/enemies/level_3/burnt_fallen_angel_attack.png",
                                    "Burnt Fallen Angel",
                                    150,
                                    3500,
                                    1500,
                                    3.5,
                                    respawn_id=self.list_of_dead_enemies[i],
                                )

                self.list_of_dead_enemies = []  # Reset the list
                self.current = self.respawn_time  # Reset the timer
        else:
            self.current -= 1
