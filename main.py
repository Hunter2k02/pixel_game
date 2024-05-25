import pygame
import os
import sys
from config import *
from entities import *
from text import Text
import random


os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 30)


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/pixel_font.ttf", 50)
        self.sky_surface = pygame.image.load("images/backgrounds/clouds.jpg")
        self.ground_surface = pygame.image.load("images/backgrounds/ground.png")
        self.window_open = True
        self.active_game = False
        self.paused_game = False
        self.buttons = [
            Text("START", AZURE, 400, 100, self.font),
            Text("EXIT", DARK_GREY, 400, 200, self.font),
        ]

        self.intro_screen()
        self.cursor_spritesheet = Spritesheet("images/cursor/cursor.jpg")
        self.shoot_cooldown_count = 0
        self.max_cooldown = 50
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.character_spritesheet = Spritesheet("images/player/player.png")
        self.terrain_spritesheet = Spritesheet("images/terrain/terrain.png")
        self.attack_spritesheet = Spritesheet("images/missles/spikes.png")
        self.ultimate_attack_spritesheet = Spritesheet("images/missles/tornado.png")

        pygame.mouse.set_visible(False)
        self.cursor = Cursor(self)

    def create_tilemap(self):
        """
        B - BLock
        P - Player
        O - Object(Tree, water sticks etc.)
        D - Decorations
        W - Water
        T - Trail
        """
        self.health_bar = Health_bar(self, 10, 10, 300, 30, 10, "red", "green")
        self.mana_bar = Bar(self, 10, 60, 300, 30, 10, "grey", LIGHTBLUE)
        self.experience_bar = Exp_bar(self, 10, 105, 300, 30, 10, "grey", "yellow")

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                random_terrain = random.randint(0, 2)
                if i < 49:

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
                                    96, 192, 32, 64, BLACK
                                ),
                                (32, 64),
                            ),
                        )

                    elif column == "B":
                        Boundary_blocks(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    994, 640, 32, 64, BLACK
                                ),
                                (128, 64),
                            ),
                        )
                    elif column == "P":
                        self.player = Player(self, j, i)
                    elif column == "e":
                        Enemy(
                            self,
                            j,
                            i,
                            "images/enemies/level_1/grey_mouse_child.png",
                            "images/enemies/level_1/grey_mouse_child_attack.png",
                            "Grey Mouse",
                            1,
                            5,
                            1,
                        ).draw(self.screen)

                    elif column == "W":
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

                else:
                    Ground(
                        self,
                        j,
                        i,
                        (
                            self.terrain_spritesheet.get_sprite(64, 352, 32, 32, WHITE),
                            (64, 64),
                        ),
                    )
                    if column == "B":
                        Boundary_blocks(
                            self,
                            j,
                            i,
                            (
                                self.terrain_spritesheet.get_sprite(
                                    994, 640, 32, 64, BLACK
                                ),
                                (64, 64),
                            ),
                        )

    def new(self):

        self.active_game = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.create_tilemap()

    def events_pause(self):
        for event in pygame.event.get():
            # Basic attack
            if (
                self.options[4].flag == 1
                and self.options[4].rect.collidepoint(pygame.mouse.get_pos())
                and self.options[4].text == "+"
            ):
                self.options[4].color = AZURE
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.basic_attack_level += 1
                    self.paused_game = False
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
                    self.player.ultimate_attack_level += 1
                    self.paused_game = False
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
                    self.player.speed_level += 1
                    self.max_cooldown -= 5
                    self.paused_game = False
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
                    self.player.health_and_mana_level += 1
                    self.paused_game = False
            elif self.options[7].text == "+":
                self.options[7].color = DARK_GREY

            if event.type == pygame.QUIT:
                pygame.quit()

    def events_main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.active_game = False
                self.window_open = False

            if self.buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                self.buttons[0].color = AZURE
                self.buttons[1].color = DARK_GREY

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.active_game = True

            else:
                self.buttons[0].color = DARK_GREY
                self.buttons[1].color = AZURE

            if self.buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                self.buttons[0].color = DARK_GREY
                self.buttons[1].color = AZURE
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pygame.quit()
                    sys.exit()

            else:
                self.buttons[0].color = AZURE
                self.buttons[1].color = DARK_GREY

    def events_in_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active_game = False
                self.window_open = False

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
            if event.type == pygame.MOUSEBUTTONDOWN and self.shoot_cooldown_count == 0:
                if event.button == 2:
                    self.experience_bar.get(100000)

            if event.type == pygame.MOUSEBUTTONDOWN and self.mana_bar.remaining >= 10:
                if event.button == 3:
                    self.mana_bar.lose(10)

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

    def cooldown(self):
        if self.shoot_cooldown_count >= self.max_cooldown:
            self.shoot_cooldown_count = 0
        elif self.shoot_cooldown_count > 0:
            self.shoot_cooldown_count += 1
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
        self.text.update()
        self.cursor.update()

    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        self.attacks.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.mana_bar.draw(self.screen)
        self.experience_bar.draw(self.screen)
        self.text.draw(self.screen)
        self.cursor.draw(self.screen)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.active_game:
            if self.paused_game:
                self.pause_screen()
            self.events_in_game()
            self.update()
            self.draw()
        self.window_open = False

    def game_over(self):
        print("Game Over")

    def intro_screen(self):
        self.screen = pygame.display.set_mode((800, 400))
        sky_x_position = 600

        while not self.active_game:

            self.screen.fill(LIGHTBLUE)
            self.screen.blit(self.sky_surface, (sky_x_position, 0))
            self.screen.blit(self.ground_surface, (0, 300))
            self.buttons[0].draw(self.screen)
            self.buttons[1].draw(self.screen)
            sky_x_position -= 0.5
            if sky_x_position <= -1200:
                sky_x_position = 700
            self.events_main_menu()
            pygame.display.update()
            self.clock.tick(FPS)

    def pause_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.options = [
            Skill_up_bar(
                self,
                WIDTH // 16,
                HEIGHT // 16,
                WIDTH * 0.75,
                HEIGHT * 0.125,
                self.player.basic_attack_level,
                12,
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
                12,
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
            pygame.display.update()
            pygame.mouse.set_visible(True)
            self.clock.tick(FPS)

        for sprite in self.options:
            sprite.kill()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))


if __name__ == "__main__":

    game = Game()
    game.new()
    while game.window_open:
        game.main()
        game.game_over()

    pygame.quit()
    sys.exit()
