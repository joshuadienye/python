# importing libraries
from typing import Any
import pygame
from os import walk
from random import choice


def random_car() -> str:
    """
    A function to select a random car object from the car object opti

    Returns:
        str: _description_
    """
    # for folder while walking through car graphics
    for folder in walk("python/frogger/graphics/cars"):
        # list generator with files in folder
        car_paths = [f"{folder[0]}/{x}" for x in folder[2]]
    return choice(car_paths)


class Car(pygame.sprite.Sprite):
    """
    A class for the cars
    """

    def __init__(self, position, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(random_car()).convert_alpha()
        self.rect = self.image.get_rect(center=position)

        # float based positioning
        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 300

        # if block for car positioning and direction
        if self.position[0] < 200:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)

        self.name = "car"
        self.hit_box = self.rect.inflate(0, -self.rect.height / 2)

    def update(self, delta_time: float, *args: Any, **kwargs: Any) -> None:
        """
        A method to update the Sprite during frame refreshes

        Args:
            delta_time (float): The time variable for screen refreshing in regards to frame rate
        """
        self.position += self.direction * self.speed * delta_time
        self.hit_box.center = (round(self.position.x), round(self.position.y))
        self.rect.center = self.hit_box.center

        # kill car if outside window
        if not -200 < self.rect.x < 3400:
            self.kill()
