# importing libraries
import pygame
import sys
from settings import *
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite
from random import choice, randint


class AllSprites(pygame.sprite.Group):
    """
    A class that represents the Sprite group class with a new method to change how objects are drawn/rendered in the window
    """

    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.offset = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.image.load(
            "python/frogger/graphics/main/map.png"
        ).convert()
        self.foreground = pygame.image.load(
            "python/frogger/graphics/main/overlay.png"
        ).convert_alpha()

    def customized_draw(self, player):
        """
        Modify how objects in the window are drawn/rendered
        """
        # changing the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit background
        self.display_surface.blit(self.background, -self.offset)

        # for sprite in group, blit on the screen
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

        self.display_surface.blit(self.foreground, -self.offset)


class Game:
    """
    A class that handles initializing the frogger game
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """
        A method to reinitialize all objects in the game
        """
        # basic setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Frogger")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player((2062, 3274), self.obstacle_sprites, self.all_sprites)

        # timer
        self.car_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.car_timer, 50)
        self.car_position_list = []

        # font
        font = pygame.font.Font(None, 50)

        # setting up
        self.setup()

        # text for winning
        self.win_text_surface = font.render(
            "YOU WON! PRESS 'R' TO RESTART", True, "white"
        )
        self.win_text_rectangle = self.win_text_surface.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

        # text for losing
        self.lose_text_surface = font.render(
            "YOU LOST! PRESS 'R' TO RETRY", True, "white"
        )
        self.lose_text_rectangle = self.lose_text_surface.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

        # music
        self.music = pygame.mixer.Sound("python/frogger/audio/music.mp3")
        self.music.play(loops=-1)

    def setup(self) -> None:
        """
        A method to set up the objects in the game
        """
        # simple sprite setup
        for file_name, position_list in SIMPLE_OBJECTS.items():
            path = f"python/frogger/graphics/objects/simple/{file_name}.png"
            surface = pygame.image.load(path).convert_alpha()
            for position in position_list:
                SimpleSprite(
                    surface, position, [self.all_sprites, self.obstacle_sprites]
                )

        # long sprite setup
        for file_name, position_list in LONG_OBJECTS.items():
            path = f"python/frogger/graphics/objects/long/{file_name}.png"
            surface = pygame.image.load(path).convert_alpha()
            for position in position_list:
                LongSprite(surface, position, [self.all_sprites, self.obstacle_sprites])

    def run(self):
        """
        A method to run the game
        """
        # game loop
        while True:
            # event loop
            for event in pygame.event.get():
                # if event is close window then quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event is car timer settig off, create random car
                if event.type == self.car_timer:
                    random_position = choice(CAR_START_POSITIONS)
                    if random_position not in self.car_position_list:
                        self.car_position_list.append(random_position)
                        position = (
                            random_position[0],
                            random_position[1] + randint(-8, 8),
                        )
                        Car(position, [self.all_sprites, self.obstacle_sprites])
                    # if car is outside the window, destroy car
                    if len(self.car_position_list) > 5:
                        del self.car_position_list[0]
                # if event is key press and key pressed is "r" and player is dead or game is finished
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_r
                        and self.player.is_dead
                        or event.key == pygame.K_r
                        and self.player.finished_game
                    ):
                        self.music.stop()
                        self.reset()

            # delta time
            delta_time = self.clock.tick() / 1000

            # fill background
            self.display_surface.fill("black")

            if self.player.is_dead:
                # player lost and lose screen should show
                self.display_surface.fill("red")
                self.display_surface.blit(
                    self.lose_text_surface, self.lose_text_rectangle
                )
            elif self.player.position.y >= 1180:
                # update
                self.all_sprites.update(delta_time=delta_time)

                # draw on display surface
                self.all_sprites.customized_draw(self.player)
            else:
                # player won and win screen should show
                self.display_surface.fill("teal")
                self.display_surface.blit(
                    self.win_text_surface, self.win_text_rectangle
                )
                self.player.finished_game = True

            # update the display surface
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
