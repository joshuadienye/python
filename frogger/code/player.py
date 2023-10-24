# importing libraries
from typing import Any
import pygame
from os import walk
from settings import *


class Player(pygame.sprite.Sprite):
    """
    A class for the player
    """

    def __init__(self, position, collision_sprites, *groups) -> None:
        super().__init__(*groups)

        # images
        self.import_assets()
        self.frame_index = 0
        self.status = "up"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=position)

        # float based positioning
        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites
        self.hit_box = self.rect.inflate(0, -self.rect.height / 2)

        # player status
        self.is_dead = False
        self.finished_game = False

    def move(self, delta_time: float) -> None:
        """
        A method to move Sprite

        Args:
            delta_time (float): The time variable for screen refreshing in regards to frame rate
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.position.x += self.direction.x * self.speed * delta_time
        self.hit_box.centerx = round(self.position.x)
        self.rect.centerx = self.hit_box.centerx
        self.collision("horizontal")

        # vertical movement
        self.position.y += self.direction.y * self.speed * delta_time
        self.hit_box.centery = round(self.position.y)
        self.rect.centery = self.hit_box.centery
        self.collision("vertical")

    def input(self) -> None:
        """
        A method to monitor keys pressed and change attributes based on keys pressed
        """
        keys = pygame.key.get_pressed()
        # horizontal movement
        if keys[pygame.K_RIGHT]:
            self.status = "right"
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = "left"
            self.direction.x = -1
        else:
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_DOWN]:
            self.status = "down"
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.status = "up"
            self.direction.y = -1
        else:
            self.direction.y = 0

    def import_assets(self) -> None:
        """
        Method to import asserts from subfolders
        """
        self.animations = {}
        for index, folder in enumerate(walk("./python/frogger/graphics/player/")):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0] + f"/{file_name}"
                    surface = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("/")[-1]
                    self.animations[key].append(surface)

    def animate(self, delta_time: float) -> None:
        """
        A method to animate the Sprites

        Args:
            delta_time (float): The time variable for screen refreshing in regards to frame rate
        """
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += 10 * delta_time
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def collision(self, direction: str) -> None:
        """
        A method to determine and react if collision between Sprites occurs

        Args:
            direction (str): The direction the Sprite is facing
        """
        if direction == "horizontal":
            for sprite in self.collision_sprites.sprites():
                if sprite.hit_box.colliderect(self.hit_box):
                    if hasattr(sprite, "name") and sprite.name == "car":
                        self.is_dead = True
                        # pygame.quit()
                        # sys.exit()
                    if self.direction.x > 0:  # player moving right
                        self.hit_box.right = sprite.hit_box.left
                        self.rect.centerx = self.hit_box.centerx
                        self.position.x = self.hit_box.centerx
                    if self.direction.x < 0:  # player moving right
                        self.hit_box.left = sprite.hit_box.right
                        self.rect.centerx = self.hit_box.centerx
                        self.position.x = self.hit_box.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hit_box.colliderect(self.hit_box):
                    if hasattr(sprite, "name") and sprite.name == "car":
                        self.is_dead = True
                        # pygame.quit()
                        # sys.exit()
                    if self.direction.y > 0:  # player moving down
                        self.hit_box.bottom = sprite.hit_box.top
                        self.rect.centery = self.hit_box.centery
                        self.position.y = self.hit_box.centery
                    if self.direction.y < 0:  # player moving up
                        self.hit_box.top = sprite.hit_box.bottom
                        self.rect.centery = self.hit_box.centery
                        self.position.y = self.hit_box.centery

    def restrict(self) -> None:
        """
        A method to restrict the movement of Sprite
        """
        if self.rect.left < 640:
            self.position.x = 640 + self.rect.width / 2
            self.hit_box.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.position.x = 2560 - self.rect.width / 2
            self.hit_box.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.position.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hit_box.centery = self.rect.centery

    def update(self, delta_time: float, *args: Any, **kwargs: Any) -> None:
        """
        A method to update the Sprite during frame refreshes

        Args:
            delta_time (float): The time variable for screen refreshing in regards to frame rate
        """
        self.input()
        self.move(delta_time)
        self.animate(delta_time)
        self.restrict()
