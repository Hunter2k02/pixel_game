from time import sleep
import pygame
from config import *


class Text:
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
    def __init__(self, game, text, color, x, y, font):
        super().__init__(text, color, x, y, font)
        self.game = game

    def update(self):
        self.text = str(f"{pygame.time.Clock.get_fps(self.game.clock):.2f}")
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)
