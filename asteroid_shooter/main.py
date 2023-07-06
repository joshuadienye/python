# importing libraries
import pygame
import sys
import random


def laser_update(laser_list, speed=300):
    for laser in laser_list:
        laser.y -= round(speed * delta_time)
        if laser.bottom < 0:
            laser_list.remove(laser)


def meteor_update(meteor_list, speed=300):
    for meteor_tuple in meteor_list:
        meteor = meteor_tuple[0]
        direction = meteor_tuple[1]
        meteor.center += direction * speed * delta_time
        # meteor.y += round(speed * delta_time)
        if meteor.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)


def display_score():
    score_text = f"Score: {pygame.time.get_ticks() // 1000}"
    surface_text = font.render(score_text, True, (255, 255, 255))
    rectangle_font = surface_text.get_rect(
        midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80)
    )
    display_surface.blit(surface_text, rectangle_font)
    pygame.draw.rect(
        display_surface,
        (255, 255, 255),
        rectangle_font.inflate(20, 20),
        width=5,
        border_radius=5,
    )


def laser_timer(can_shoot, duration=500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot


# setting width and height
FONT_STYLE = "python/asteroid_shooter/graphics/subatomic.ttf"
IMAGE_BACKGROUND = "python/asteroid_shooter/graphics/background.png"
IMAGE_LASER = "python/asteroid_shooter/graphics/laser.png"
IMAGE_METEOR = "python/asteroid_shooter/graphics/meteor.png"
IMAGE_SHIP = "python/asteroid_shooter/graphics/ship.png"
SOUND_EXPLOSION = "python/asteroid_shooter/sounds/explosion.wav"
SOUND_LASER = "python/asteroid_shooter/sounds/laser.ogg"
SOUND_MUSIC = "python/asteroid_shooter/sounds/music.wav"
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# initializing pygame
pygame.init()
display_surface = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)  # creating display
pygame.display.set_caption("Meteor Shooter")  # changing window title
clock = pygame.time.Clock()  # setting clock

# creating background
surface_backgound = pygame.image.load(IMAGE_BACKGROUND).convert()

# creating ship and ship rectangle
surface_ship = pygame.image.load(IMAGE_SHIP).convert_alpha()
rectangle_ship = surface_ship.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# creating laser and laser rectangle
surface_laser = pygame.image.load(IMAGE_LASER).convert_alpha()
laser_list = []
# rectangle_laser = surface_laser.get_rect(midbottom=rectangle_ship.midtop)

# creating ship and ship rectangle
surface_meteor = pygame.image.load(IMAGE_METEOR).convert_alpha()
meteor_list = []

# laser timer
can_shoot = True
shoot_time = None

# creating font and font rectangle
font = pygame.font.Font(FONT_STYLE, 50)

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

sound_laser = pygame.mixer.Sound(SOUND_LASER)
sound_explosion = pygame.mixer.Sound(SOUND_EXPLOSION)
sound_background = pygame.mixer.Sound(SOUND_MUSIC)

sound_background.play(loops=-1)

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            rectangle_laser = surface_laser.get_rect(midbottom=rectangle_ship.midtop)
            laser_list.append(rectangle_laser)
            can_shoot = False
            shoot_time = pygame.time.get_ticks()
            sound_laser.play()
        if event.type == meteor_timer:
            # random position
            x_position = random.randint(-100, WINDOW_WIDTH + 100)
            y_position = random.randint(-100, -50)

            # create meteor
            rectangle_meteor = surface_meteor.get_rect(center=(x_position, y_position))

            direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
            meteor_list.append((rectangle_meteor, direction))

    # frame rate limit
    delta_time = clock.tick(120) / 1000  # in seconds

    # mouse input
    rectangle_ship.center = pygame.mouse.get_pos()

    laser_update(laser_list)
    meteor_update(meteor_list)
    can_shoot = laser_timer(can_shoot, 400)

    # meteor - ship collisions
    for meteor_tuple in meteor_list:
        meteor = meteor_tuple[0]
        if rectangle_ship.colliderect(meteor):
            pygame.quit()
            sys.exit()

    # meteor - laser collisions
    for meteor_tuple in meteor_list:
        for laser in laser_list:
            if laser.colliderect(meteor_tuple[0]):
                sound_explosion.play()
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser)

    # pygame.time.get_ticks()

    # drawing surfaces
    # display_surface.fill((200, 200, 200))
    display_surface.blit(surface_backgound, (0, 0))
    display_score()
    for laser in laser_list:
        display_surface.blit(surface_laser, laser)
    for meteor_tuple in meteor_list:
        display_surface.blit(surface_meteor, meteor_tuple[0])
    display_surface.blit(surface_ship, rectangle_ship)

    # updates display surface
    pygame.display.update()
