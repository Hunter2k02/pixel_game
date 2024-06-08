import pygame
from config import *


class Text:
    """
    A class representing text to be displayed on the screen.

    Attributes:
        text (str): The text to be displayed.
        color (tuple): The color of the text in RGB format.
        x (int): The x-coordinate of the text's position.
        y (int): The y-coordinate of the text's position.
        font (pygame.font.Font): The font used for the text.

    Methods:
        update(): Updates the text's image and position.
        draw(surface): Draws the text on the given surface.
    """

    def __init__(self, text, color, x, y, font):
        self.text = str(text)
        self.color = color
        self.x = x
        self.y = y
        self.font = font

    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)


class Temporary_text_experience(pygame.sprite.Sprite):
    """
    A class representing temporary text experience in a pygame game.

    Attributes:
        game (Game): The game instance.
        text (str): The text to be displayed.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        font (Font): The font used for the text.
        end_time (int): The time when the text should disappear.
        amount (int): The amount of text experiences.

    Methods:
        update(): Updates the text experience.
        draw(screen): Draws the text on the screen.
    """

    def __init__(self, game, text, color, x, y, font):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.text
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.text = str(text)
        self.color = color
        self.x = x
        lenght = len(
            [
                x
                for x in self.game.text
                if x.__class__.__name__ == "Temporary_text_experience"
            ]
        )
        self.y = y + 25 * (lenght - 1)
        self.font = font
        self.end_time = pygame.time.get_ticks() + 5000
        self.amount = 0

    def update(self):
        self.draw(self.game.screen)

    def draw(self, screen):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.image, self.rect)
        if pygame.time.get_ticks() > self.end_time:
            self.kill()


class Temporary_text_damage(pygame.sprite.Sprite):
    """
    A class representing temporary text damage in a game.

    Attributes:
        game (Game): The game instance.
        text (str): The text to be displayed.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        font (Font): The font used for the text.
        end_time (int): The time when the text should disappear.
        amount (int): The amount of damage.

    Methods:
        update(): Updates the state of the text damage.
        draw(screen): Draws the text on the screen.
    """

    def __init__(self, game, text, color, x, y, font):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.text
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.text = str(text)
        self.color = color
        self.x = x
        self.y = y
        self.font = font
        self.end_time = pygame.time.get_ticks() + 1000
        self.amount = 0

    def update(self):
        self.draw(self.game.screen)

    def draw(self, screen):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        screen.blit(self.image, self.rect)
        if pygame.time.get_ticks() > self.end_time:
            self.kill()


class Level_up_text(pygame.sprite.Sprite):
    """
    A class representing a level up text in a game.

    Attributes:
        game (Game): The game instance.
        text (str): The text to be displayed.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text position.
        y (int): The y-coordinate of the text position.
        font (Font): The font used for rendering the text.
        amount (int): The amount of the text.
        flag (int): A flag indicating whether the text should be displayed or not.
    """

    def __init__(self, game, text, color, x, y, font):
        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.text
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.text = str(text)
        self.color = color
        self.x = x
        self.y = y
        self.font = font
        self.amount = 0
        self.flag = 1

    def update(self):
        self.draw(self.game.screen)

    def draw(self, screen):
        if self.flag:
            self.image = self.font.render(self.text, 1, self.color)
            self.rect = self.image.get_rect()
            self.rect.center = self.x, self.y
            screen.blit(self.image, self.rect)

    def delete(self):
        self.flag = 0


class Show_FPS(Text):
    """
    A class that represents a text object displaying the frames per second (FPS) in a game.

    Attributes:
        game (Game): The game object.
        text (str): The text to be displayed.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text position.
        y (int): The y-coordinate of the text position.
        font (Font): The font used for rendering the text.

    Methods:
        update(): Updates the text and image based on the current FPS.
        draw(surface): Draws the text on the given surface.
    """

    def __init__(self, game, text, color, x, y, font):
        super().__init__(text, color, x, y, font)
        self.game = game

    def update(self):
        self.text = str(f"fps: {pygame.time.Clock.get_fps(self.game.clock):.2f}")
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)
