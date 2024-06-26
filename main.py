import pygame
import os
import sys
from config import *
from entities import *
from text import Text
import random

# Setting the position of the window to left top corner
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 30)
# setting global variable to check if the game has ended
game_ended = 0
# setting the flags for the window
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF


class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.music = Music()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/pixel_font.ttf", 50)
        self.win = 0
        self.window_open = 1
        self.active_game = 0
        self.paused_game = 0

        self.buttons = [
            Text("START", AZURE, 400, 100, self.font),
            Text("EXIT", DARK_GREY, 400, 200, self.font),
        ]

        pygame.mouse.set_visible(False)
        self.intro_screen()
        self.FPS = Show_FPS(
            self,
            pygame.time.Clock.get_fps(self.clock),
            WHITE,
            WIDTH - WIDTH * 0.05,
            HEIGHT * 0.05,
            pygame.font.Font("font/pixel_font.ttf", 30),
        )
        self.shoot_cooldown_count = 0
        self.max_cooldown = 50
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.character_spritesheet = Spritesheet("images/player/player.png")
        self.terrain_spritesheet = Spritesheet("images/terrain/terrain.png")
        self.attack_spritesheet = Spritesheet("images/missles/spikes.png")
        self.ultimate_attack_spritesheet = Spritesheet("images/missles/tornado.png")
        self.skull_spritesheet = Spritesheet("images/enemies/level_2/skull.png")
        self.mana_cost = 10

    def create_tilemap(self):

        self.health_bar = Health_bar(self, 10, 10, 300, 30, 10, "red", "green")
        self.mana_bar = Bar(self, 10, 60, 300, 30, 10, "grey", LIGHTBLUE)
        self.experience_bar = Exp_bar(self, 10, 105, 300, 30, 10, "grey", "yellow")
        """
        1 level:
        B - BLock
        P - Player
        O - Object(Tree, water sticks etc.)
        D - Decorations
        A - Water
        T - Trail
        Enemies:
        e - Grey Mouse
        a - Brown Mouse
        s - White Mouse
        b - Boss Mouse
        2 level:
        T- Trail
        r - Small Rock
        R - Big Rock
        Enemies:
        b - Desert Boarman
        w - Desert Wolf
        W - Desert Wartotaur
        M - Desert Minotaur Boss
        3 level:
        T- Trail
        s - Skull
        H - Hole
        L - Lava
        Enemies:
        i - Burnt Imp
        u - Burnt Succubus
        f - Burnt Fallen Angel
        4 level:
        T- Trail
        s - Skull
        Enemies:
        E - Dragon
        """
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):

                random_terrain = random.randint(0, 2)
                if column == "B":
                    Block(
                        self,
                        j,
                        i,
                        (
                            self.terrain_spritesheet.get_sprite(
                                994, 643, 25, 64, WHITE
                            ),
                            (64, 64),
                        ),
                    )
                    # 288 575

                if i < 48 and j < 100:

                    if random_terrain == 1:
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    64, 352, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif random_terrain == 2:
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    96, 352, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )

                    else:
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    1, 352, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )

                    if column == "T":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    27, 89, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif column == "O":
                        Block(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    43, 832, 64, 64, BLACK
                                ),
                                (64, 64),
                            ),
                        )
                    if column == "D":
                        Block(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    96, 202, 32, 54, WHITE
                                ),
                                (32, 64),
                            ),
                        )
                    elif column == "e":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_1/grey_mouse_child.png",
                            "images/enemies/level_1/grey_mouse_child_attack.png",
                            "Grey Mouse",
                            2,
                            10,
                            2,
                            1.35,
                        )
                    elif column == "a":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_1/brown_mouse_assassin.png",
                            "images/enemies/level_1/brown_mouse_assassin_attack.png",
                            "Brown Mouse",
                            6,
                            20,
                            5,
                            2,
                        )
                    elif column == "s":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_1/white_mouse_spearman.png",
                            "images/enemies/level_1/white_mouse_spearman_attack.png",
                            "White Mouse",
                            15,
                            50,
                            30,
                            2.25,
                        )
                    elif column == "b":
                        Boss(
                            self,
                            j,
                            i,
                            "images/enemies/level_1/mouse_boss.png",
                            "images/enemies/level_1/mouse_boss_attack.png",
                            "images/enemies/level_1/mouse_boss_boss_attack.png",
                            "Boss Mouse",
                            25,
                            200,
                            100,
                            2.5,
                        )

                    elif column == "A":
                        Block(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    891, 90, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )

                elif i >= 48 and i < 71 and j < 99:
                    Ground(
                        self,
                        j,
                        i,
                        (
                            self.terrain_spritesheet.get_sprite(
                                576 + 32 * random.randint(0, 2), 352, 32, 32, WHITE
                            ),
                            (64, 64),
                        ),
                    )
                    if column == "b":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_2/desert_boarman.png",
                            "images/enemies/level_2/desert_boarman_attack.png",
                            "Desert Boarman",
                            25,
                            225,
                            75,
                            2.25,
                        )
                    elif column == "w":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_2/desert_wolf.png",
                            "images/enemies/level_2/desert_wolf_attack.png",
                            "Desert Wolf",
                            35,
                            250,
                            125,
                            2.75,
                        )
                    elif column == "W":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_2/desert_wartotaur.png",
                            "images/enemies/level_2/desert_wartotaur_attack.png",
                            "Desert Wartotaur",
                            55,
                            500,
                            250,
                            2.5,
                        )
                    elif column == "M":
                        Boss(
                            self,
                            j,
                            i,
                            "images/enemies/level_2/desert_minotaur_boss.png",
                            "images/enemies/level_2/skull.png",
                            "images/enemies/level_2/desert_minotaur_boss_attack.png",
                            "Desert Boss",
                            40,
                            2500,
                            1000,
                            3.0,
                        )
                    elif column == "T":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    120, 86, 50, 50, WHITE
                                ),
                                (64, 64),
                            ),
                        )

                    elif column == "r":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    0, 0, 32, 64, WHITE
                                ),
                                (32, 64),
                            ),
                        )
                    elif column == "R":
                        r = random.randint(1, 3)
                        if r == 1:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        768, 624, 64, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                        elif r == 2:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        832, 624, 64, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                        elif r == 3:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        897, 624, 30, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                    elif column == "s":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.skull_spritesheet.get_sprite(
                                    0, 128, 64, 64, WHITE
                                ),
                                (64, 64),
                            ),
                        )

                elif i >= 71 and j < 99:

                    # Base
                    Ground(
                        self,
                        j,
                        i,
                        (
                            self.terrain_spritesheet.get_sprite(
                                288 + 32 * random.randint(0, 2), 160, 32, 32, WHITE
                            ),
                            (64, 64),
                        ),
                    )

                    # Enemies
                    if column == "i":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_3/burnt_imp.png",
                            "images/enemies/level_3/burnt_imp_attack.png",
                            "Burnt Imp",
                            75,
                            750,
                            375,
                            3.0,
                        )
                    elif column == "u":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_3/burnt_succubus.png",
                            "images/enemies/level_3/burnt_succubus_attack.png",
                            "Burnt Succubus",
                            100,
                            1500,
                            750,
                            3.25,
                        )
                    elif column == "f":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_3/burnt_fallen_angel.png",
                            "images/enemies/level_3/burnt_fallen_angel_attack.png",
                            "Burnt Fallen Angel",
                            150,
                            3500,
                            1500,
                            3.5,
                        )

                    # Blocks and decorations
                    elif column == "H":

                        Block(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    512, 0, 64, 64, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif column == "L":
                        Block(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    480 + 32 * random.randint(0, 2), 160, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif column == "T":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    416 + 32 * random.randint(0, 1), 160, 32, 32, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif column == "R":
                        r = random.randint(1, 3)
                        if r == 1:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        768, 690, 64, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                        elif r == 2:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        832, 690, 64, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                        elif r == 3:
                            Block(
                                self,
                                j,
                                i,
                                (
                                    self.terrain_spritesheet.get_sprite(
                                        897, 690, 30, 50, WHITE
                                    ),
                                    (64, 64),
                                ),
                            )
                    elif column == "s":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.skull_spritesheet.get_sprite(
                                    0, 128, 64, 64, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                if i > 45 and j > 98:

                    Ground(
                        self,
                        j,
                        i,
                        (
                            self.terrain_spritesheet.get_sprite(
                                96 + 32 * random.randint(0, 2), 544, 32, 32, WHITE
                            ),
                            (64, 64),
                        ),
                    )
                    if column == "S":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    288, 575, 64, 64, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    elif column == "s":
                        Ground(
                            self,
                            j,
                            i,
                            (
                                self.skull_spritesheet.get_sprite(
                                    0, 128, 64, 64, WHITE
                                ),
                                (64, 64),
                            ),
                        )
                    # Final Boss
                    elif column == "E":
                        Last_boss(
                            self,
                            j,
                            i,
                            "images/enemies/level_4/dragon.png",
                            "images/enemies/level_4/dragon_basic.png",
                            "images/enemies/level_4/dragon_ultimate.png",
                            "Dragon",
                            300,
                            9999,
                            19999,
                            7,
                        )

        self.player = Player(self, WIDTH // 128, HEIGHT // 128)
        self.spawner = Spawner(self)

    def new(self):

        self.active_game = 1
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.create_tilemap()

    def events_game_over(self):
        """
        Handle events for the game over screen.

        This method is responsible for handling events such as mouse clicks and quitting the game.
        It sets the allowed event types to pygame.QUIT and pygame.MOUSEBUTTONDOWN.
        It checks for mouse clicks on the game over screen options and performs the corresponding actions.

        Args:
            None

        Returns:
            None
        """
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
        global game_ended
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if self.options[0].rect.collidepoint(pygame.mouse.get_pos()):
                self.options[0].color = "red"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    game_ended = 0
                    self.window_open = 0
                    break

            else:
                self.options[0].color = DARK_GREY

            if self.options[1].rect.collidepoint(pygame.mouse.get_pos()):
                self.options[1].color = "red"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    game_ended = 1
                    self.window_open = 0

            else:
                self.options[1].color = DARK_GREY

    def events_pause(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
        for event in pygame.event.get():
            # Basic attack
            if (
                self.options[4].flag == 1
                and self.options[4].rect.collidepoint(pygame.mouse.get_pos())
                and self.options[4].text == "+"
            ):
                self.options[4].color = AZURE
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    self.player.basic_attack_level += 1

                    self.health_bar.remaining = self.health_bar.full
                    self.mana_bar.remaining = self.mana_bar.full
                    self.paused_game = 0
            elif self.options[4].text == "+":
                self.options[4].color = DARK_GREY
            # Ultimate attack
            if (
                self.options[5].flag == 1
                and self.options[5].rect.collidepoint(pygame.mouse.get_pos())
                and self.options[5].text == "+"
            ):
                self.options[5].color = AZURE

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    self.player.ultimate_attack_level += 1

                    self.mana_cost = int(self.mana_cost * 1.25)
                    self.health_bar.remaining = self.health_bar.full
                    self.mana_bar.remaining = self.mana_bar.full
                    self.paused_game = 0
            elif self.options[5].text == "+":
                self.options[5].color = DARK_GREY
            # Speed
            if (
                self.options[6].flag == 1
                and self.options[6].rect.collidepoint(pygame.mouse.get_pos())
                and self.options[6].text == "+"
            ):
                self.options[6].color = AZURE

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    self.player.speed_level += 1
                    self.player.player_speed = (
                        PLAYER_SPEED + self.player.speed_level // 4
                    )
                    self.max_cooldown -= 2
                    self.health_bar.remaining = self.health_bar.full
                    self.mana_bar.remaining = self.mana_bar.full
                    self.paused_game = 0
            elif self.options[6].text == "+":
                self.options[6].color = DARK_GREY
            # Hp/Mana
            if (
                self.options[7].flag == 1
                and self.options[7].rect.collidepoint(pygame.mouse.get_pos())
                and self.options[7].text == "+"
            ):
                self.options[7].color = AZURE

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    self.player.health_and_mana_level += 1
                    self.mana_bar.full += 10 * self.player.health_and_mana_level
                    self.mana_bar.regen += self.mana_bar.regen * 0.25
                    self.health_bar.full += (
                        10 * self.player.health_and_mana_level
                        + int(self.health_bar.full * 0.25)
                    )
                    self.health_bar.regen += self.health_bar.regen * 0.4
                    self.mana_bar.remaining = self.mana_bar.full
                    self.health_bar.remaining = self.health_bar.full
                    self.paused_game = 0
            elif self.options[7].text == "+":
                self.options[7].color = DARK_GREY

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused_game = 0

    def events_main_menu(self):
        """
        Handle events for the main menu.

        This method is responsible for handling events related to the main menu of the game.
        It checks for various events such as mouse clicks, keyboard inputs, and window close events.
        Based on the events, it performs different actions such as changing button colors, playing sounds, and quitting the game.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.active_game = 0
                self.window_open = 0

            if self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                self.buttons[0].color = AZURE
                self.buttons[1].color = DARK_GREY

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    pygame.mixer.music.stop()
                    self.active_game = 1

            else:
                self.buttons[0].color = DARK_GREY
                self.buttons[1].color = AZURE

            if self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                self.buttons[0].color = DARK_GREY
                self.buttons[1].color = AZURE

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    pygame.mixer.music.stop()
                    pygame.time.wait(500) #Needed for button click sound before exiting program
                    pygame.quit()
                    sys.exit()

            else:
                self.buttons[0].color = AZURE
                self.buttons[1].color = DARK_GREY

    def events_in_game(self):
        """
        Handle the events that occur during the game.

        This method is responsible for processing various events such as quitting the game,
        shooting projectiles, using ultimate attacks, and gaining experience.

        Args:
            None

        Returns:
            None
        """
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and self.shoot_cooldown_count == 0:

                if event.button == 1:
                    self.shoot_cooldown_count += 1
                    if self.player.facing == "up":

                        Attack(
                            self, self.player.rect.x, self.player.rect.y - TILESIZE // 2
                        )
                    if self.player.facing == "down":
                        Attack(
                            self, self.player.rect.x, self.player.rect.y + TILESIZE // 2
                        )
                    if self.player.facing == "left":
                        Attack(
                            self, self.player.rect.x - TILESIZE // 2, self.player.rect.y
                        )
                    if self.player.facing == "right":
                        Attack(
                            self, self.player.rect.x + TILESIZE // 2, self.player.rect.y
                        )

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.mana_bar.remaining >= self.mana_cost
            ):
                if event.button == 3:
                    self.mana_bar.lose(self.mana_cost)

                    if self.player.facing == "up":
                        Ultimate_attack(
                            self, self.player.rect.x, self.player.rect.y - TILESIZE
                        )
                    if self.player.facing == "down":
                        Ultimate_attack(
                            self, self.player.rect.x, self.player.rect.y + TILESIZE
                        )
                    if self.player.facing == "left":
                        Ultimate_attack(
                            self, self.player.rect.x - TILESIZE, self.player.rect.y
                        )
                    if self.player.facing == "right":
                        Ultimate_attack(
                            self, self.player.rect.x + TILESIZE, self.player.rect.y
                        )
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.experience_bar.get(10000)

    def events_end_screen(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
        global game_ended
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if self.options[0].rect.collidepoint(pygame.mouse.get_pos()):
                self.options[0].color = GOLD
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.music.play_sound("button_click")
                    game_ended = 0
                    self.window_open = 0
                    break

            else:
                self.options[0].color = FIRE

    def cooldown(self):
        # Cooldown for the basic attack
        if self.shoot_cooldown_count >= self.max_cooldown:
            self.shoot_cooldown_count = 0
        elif self.shoot_cooldown_count > 0:
            self.shoot_cooldown_count += 1
        if self.mana_bar.remaining != self.mana_bar.full:
            self.mana_bar.get()
        if self.health_bar.remaining != self.health_bar.full:
            self.health_bar.get()

    def update(self):
        # Update everything
        self.cooldown()
        self.all_sprites.update()
        self.attacks.update()
        self.health_bar.update()
        self.mana_bar.update()
        self.experience_bar.update()
        self.text.update()
        self.FPS.update()
        self.spawner.update()
        self.cursor.update()

    def draw(self):
        # Draw everything
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.attacks.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.mana_bar.draw(self.screen)
        self.experience_bar.draw(self.screen)
        self.text.draw(self.screen)
        self.FPS.draw(self.screen)
        self.cursor.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Main game loop
        while self.active_game:

            if self.paused_game:
                self.pause_screen()
            self.events_in_game()
            self.update()
            self.draw()
        if self.win:
            self.end_screen()
        else:
            self.game_over()

    def game_over(self):
        # Game over screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.options = [
            Text(
                "Retry",
                DARK_GREY,
                WIDTH // 2,
                HEIGHT * 0.65,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Text(
                "EXIT",
                DARK_GREY,
                WIDTH // 2,
                HEIGHT * 0.85,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Text(
                "GAME OVER",
                RED,
                WIDTH // 2,
                HEIGHT * 0.3,
                pygame.font.Font("font/pixel_font.ttf", 170),
            ),
        ]

        pygame.time.wait(1000)
        self.music.play_sound("game_over")
        while self.window_open:
            self.screen.fill(BLACK)

            for sprite in self.options:
                sprite.draw(self.screen)
            self.cursor.draw(self.screen)
            self.cursor.update()
            pygame.display.update()
            self.clock.tick(FPS)
            self.events_game_over()

    def intro_screen(self):
        self.screen = pygame.display.set_mode((800, 400))
        self.sky_surface = pygame.image.load("images/backgrounds/clouds.jpg").convert()
        self.ground_surface = pygame.image.load(
            "images/backgrounds/ground.png"
        ).convert()
        self.cursor_spritesheet = Spritesheet("images/cursor/cursor.jpg")
        self.cursor = Cursor(self)
        sky_x_position = 600

        self.music.play_music("main_menu")
        pygame.mixer.music.set_volume(0.25)  # 25% volume
        while not self.active_game:

            self.screen.fill(LIGHTBLUE)
            self.screen.blit(self.sky_surface, (sky_x_position, 0))
            self.screen.blit(self.ground_surface, (0, 300))
            self.buttons[0].draw(self.screen)
            self.buttons[1].draw(self.screen)
            sky_x_position -= 0.5
            if sky_x_position <= -1200:
                sky_x_position = 700
            self.cursor.draw(self.screen)
            self.cursor.update()
            self.events_main_menu()
            pygame.display.update()
            self.clock.tick(FPS)

    def pause_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

        self.music.play_sound("level_up")
        # All the options for the pause screen
        self.options = [
            Skill_up_bar(
                self,
                WIDTH // 16,
                HEIGHT // 16,
                WIDTH * 0.75,
                HEIGHT * 0.125,
                self.player.basic_attack_level,
                15,
                "grey",
                "blue",
            ),
            Skill_up_bar(
                self,
                WIDTH // 16,
                HEIGHT // 4 + HEIGHT // 16,
                WIDTH * 0.75,
                HEIGHT * 0.125,
                self.player.ultimate_attack_level,
                12,
                "grey",
                "blue",
            ),
            Skill_up_bar(
                self,
                WIDTH // 16,
                HEIGHT // 2 + HEIGHT // 16,
                WIDTH * 0.75,
                HEIGHT * 0.125,
                self.player.speed_level,
                10,
                "grey",
                "blue",
            ),
            Skill_up_bar(
                self,
                WIDTH // 16,
                HEIGHT // 2 + HEIGHT // 4 + HEIGHT // 16,
                WIDTH * 0.75,
                HEIGHT * 0.125,
                self.player.health_and_mana_level,
                15,
                "grey",
                "blue",
            ),
            Level_up_text(
                self,
                "+",
                AZURE,
                WIDTH * 0.85,
                HEIGHT // 8,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Level_up_text(
                self,
                "+",
                AZURE,
                WIDTH * 0.85,
                HEIGHT // 4 + HEIGHT // 8,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Level_up_text(
                self,
                "+",
                AZURE,
                WIDTH * 0.85,
                HEIGHT // 2 + HEIGHT // 8,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Level_up_text(
                self,
                "+",
                AZURE,
                WIDTH * 0.85,
                HEIGHT // 2 + HEIGHT // 4 + HEIGHT // 8 + 5,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Level_up_text(
                self,
                "Basic Attack",
                AZURE,
                WIDTH // 16 + WIDTH * 0.375,
                HEIGHT // 32 - 5,
                pygame.font.Font("font/pixel_font.ttf", 50),
            ),
            Level_up_text(
                self,
                "Ultimate Attack",
                AZURE,
                WIDTH // 16 + WIDTH * 0.375,
                HEIGHT // 4 + HEIGHT // 32 - 5,
                pygame.font.Font("font/pixel_font.ttf", 50),
            ),
            Level_up_text(
                self,
                "Speed, Missle Velocity/Range",
                AZURE,
                WIDTH // 16 + WIDTH * 0.375,
                HEIGHT // 2 + HEIGHT // 32 - 5,
                pygame.font.Font("font/pixel_font.ttf", 50),
            ),
            Level_up_text(
                self,
                "Max Health, Mana/ Regeneration Health, Mana",
                AZURE,
                WIDTH // 16 + WIDTH * 0.375,
                HEIGHT // 2 + HEIGHT // 4 + HEIGHT // 32 - 5,
                pygame.font.Font("font/pixel_font.ttf", 50),
            ),
        ]
        for i in range(4):
            if self.options[i].current >= self.options[i].full:
                self.options[i + 4].kill()
                self.options[i + 4].delete()

        while self.paused_game:

            self.screen.fill(PANTONE)
            for sprite in self.options:
                sprite.update()
                sprite.draw(self.screen)

            self.events_pause()
            self.cursor.draw(self.screen)
            self.cursor.update()
            pygame.display.update()

            self.clock.tick(FPS)

        for sprite in self.options:
            sprite.kill()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    def end_screen(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        # All the options for the end screen
        self.options = [
            Text(
                "ADVENTURE AGAIN?",
                FIRE,
                WIDTH // 2,
                HEIGHT * 0.85,
                pygame.font.Font("font/pixel_font.ttf", 100),
            ),
            Text(
                "YOU                          WIN!",
                FIRE,
                WIDTH // 2,
                HEIGHT * 0.3,
                pygame.font.Font("font/pixel_font.ttf", 170),
            ),
        ]
        pygame.time.wait(1000)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.music.play_music("victory")
        pygame.mixer.music.set_volume(0.5)
        self.image = pygame.image.load(
            "images/enemies/level_4/dragon_skull.png"
        ).convert()

        while self.window_open:
            self.screen.fill(BLACK)
            self.screen.blit(self.image, (WIDTH * 0.21, 0))
            for sprite in self.options:
                sprite.draw(self.screen)
            self.cursor.draw(self.screen)
            self.cursor.update()
            pygame.display.update()
            self.clock.tick(FPS)
            self.events_end_screen()


if __name__ == "__main__":

    while not game_ended:
        game = Game()
        game.new()
        while game.window_open:
            game.main()
