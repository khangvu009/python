import pygame
import random
import os
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BRIGHT_YELLOW = (255, 223, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plants vs Zombies")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def load_gif_with_pillow(filename, target_width, target_height):
    pil_image = Image.open(filename)
    frames = []
    while True:
        mode = pil_image.mode
        size = pil_image.size
        palette = pil_image.getpalette()
        pygame_image = pygame.image.fromstring(pil_image.tobytes(), size, mode)
        pygame_image = pygame.transform.scale(pygame_image, (target_width, target_height))
        frames.append(pygame_image)
        try:
            pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            break
    return frames

# # Assuming the peashooter GIF has frames horizontally arranged with equal width
# peashooter_frame_count = 498 // 332  # Calculate the number of frames
# sunflower_frame_count = 1  # Since the sunflower image is 640x640, it's likely a single frame

# Load GIF frames and resize them to fit the hitbox
sunflower_target_size = (64, 64)  # Target size for sunflower
peashooter_target_size = (64, 64)  # Target size for peashooter
# zombie_target_size = (64, 64)  # Target size for zombie

sunflower_frames = load_gif_with_pillow("C:\\python\\zombie_vs_plant\\sunflower.gif",sunflower_target_size)
peashooter_frames = load_gif_with_pillow("C:\\python\\zombie_vs_plant\\peashooter.gif",peashooter_target_size)

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = peashooter_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.shoot_delay = 1000  # Delay in milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.animation_delay = 100  # Delay between animation frames in milliseconds
        self.last_update = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return Projectile(self.rect.centerx + 25, self.rect.centery)
        return None

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Sunflower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = sunflower_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.sun_delay = 5000  # Delay in milliseconds for generating sun points
        self.last_sun = pygame.time.get_ticks()
        self.animation_delay = 100  # Delay between animation frames in milliseconds
        self.last_update = pygame.time.get_ticks()

    def generate_sun(self):
        now = pygame.time.get_ticks()
        if now - self.last_sun > self.sun_delay:
            self.last_sun = now
            return Sun(self.rect.centerx, self.rect.centery)
        return None

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Sun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BRIGHT_YELLOW)  # Bright yellow color for sun points
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 5000  # Sun points last for 5 seconds
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.lifetime:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.x += self.speed

# Sprite groups
all_sprites = pygame.sprite.Group()
plants = pygame.sprite.Group()
zombies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
suns = pygame.sprite.Group()

# Create plants, sunflowers, and zombies
plant = Plant(100, SCREEN_HEIGHT // 2)
sunflower = Sunflower(200, SCREEN_HEIGHT // 2)
zombie = Zombie(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

all_sprites.add(plant)
all_sprites.add(sunflower)
all_sprites.add(zombie)
plants.add(plant)
plants.add(sunflower)
zombies.add(zombie)

# Track collected sun points
sun_points = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for sun in suns:
                if sun.rect.collidepoint(pos):
                    sun.kill()
                    sun_points += 1

    # Update all sprites
    all_sprites.update()

    # Plant shoots
    projectile = plant.shoot()
    if projectile:
        all_sprites.add(projectile)
        projectiles.add(projectile)

    # Sunflower generates sun points
    sun = sunflower.generate_sun()
    if sun:
        all_sprites.add(sun)
        suns.add(sun)

    # Check for collisions between projectiles and zombies
    hits = pygame.sprite.groupcollide(projectiles, zombies, True, True)

    # Draw everything
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Display collected sun points
    font = pygame.font.Font(None, 36)
    text = font.render(f"Sun Points: {sun_points}", True, WHITE)
    screen.blit(text, (10, 10))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
