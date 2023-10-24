# importing libraries
import pygame


class SimpleSprite(pygame.sprite.Sprite):
    """
    A class for Sprites with a regular hit box
    """

    def __init__(self, surface, position, *groups) -> None:
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(0, -self.rect.height / 2)


class LongSprite(pygame.sprite.Sprite):
    """
    A class for Sprites with a long hit box
    """

    def __init__(self, surface, position, *groups) -> None:
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(-self.rect.width * 0.8, -self.rect.height / 2)
        self.hit_box.bottom = self.rect.bottom - 10
