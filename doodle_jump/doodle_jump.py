import pygame
import os
import sys
import win32com.client
import random

def create_or_update_shortcut(window_title, icon_path):
    try:
        # Get the absolute path of the script
        script_path = os.path.abspath(__file__)

        # Specify Python executable (use pythonw.exe explicitly)
        pythonw_exe = r'C:\Users\YourUsername\AppData\Local\Programs\Python\Python3.12.4\pythonw.exe'

        # Create shortcut path
        shortcut_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'{window_title}.lnk')

        # Initialize Shell object
        shell = win32com.client.Dispatch("WScript.Shell")

        # Check if the shortcut already exists
        if os.path.exists(shortcut_path):
            # Get existing shortcut
            shortcut = shell.CreateShortcut(shortcut_path)

            # Check if existing shortcut needs update
            if (shortcut.TargetPath.lower() != pythonw_exe.lower() or 
                shortcut.Arguments.lower() != f'"{script_path}"' or 
                shortcut.IconLocation.lower() != icon_path.lower()):
                # Update the shortcut properties
                shortcut.TargetPath = pythonw_exe
                shortcut.Arguments = f'"{script_path}"'
                shortcut.IconLocation = icon_path
                shortcut.Save()
                print(f"Shortcut updated: {shortcut_path}")
            else:
                print(f"Shortcut already up-to-date: {shortcut_path}")
        else:
            # Create new shortcut
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = pythonw_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.IconLocation = icon_path
            shortcut.Save()
            print(f"Shortcut created with icon: {shortcut_path}")

    except Exception as e:
        print(f"Error creating or updating shortcut: {e}")

# Initialize Pygame
pygame.init()

# Set window title and icon path
window_title = "Doodle jump"
icon_path = r"C:\python\doodle_jump\icon.ico"  # Replace with the path to your .ico file
script_to_run = os.path.abspath(__file__)

# Create or update the shortcut with the icon
create_or_update_shortcut(window_title, icon_path)

# Set up window size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle jump")
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 1
SCROLL_THRESH = 200
bg_scroll = 0
MAX_PLATFORMS = 10

# Load images
bg_image = pygame.image.load("C:\\python\\doodle_jump\\bg.png")
jumpy_image = pygame.image.load("C:\\python\\doodle_jump\\jump.png").convert_alpha()
platform_image = pygame.image.load("C:\\python\\doodle_jump\\wood.png").convert_alpha()
bird_sheet = pygame.image.load("C:\\python\\doodle_jump\\bird.png").convert_alpha()
spring_image = pygame.image.load("C:\\python\\doodle_jump\\wood.png").convert_alpha()
icon = pygame.image.load("C:\\python\\doodle_jump\\icon.ico")

# Bird animation settings
BIRD_FRAMES = 9
BIRD_WIDTH = bird_sheet.get_width() // BIRD_FRAMES
BIRD_HEIGHT = bird_sheet.get_height()

# Extract bird frames from sprite sheet
bird_frames = []
for i in range(BIRD_FRAMES):
    frame = bird_sheet.subsurface((i * BIRD_WIDTH, 0, BIRD_WIDTH, BIRD_HEIGHT))
    bird_frames.append(frame)

jumpy_height = jumpy_image.get_rect().height
jumpy_width = jumpy_image.get_rect().width

WHITE = (255, 255, 255)

def draw_bg(scroll):
    screen.blit(bg_image, (0, 0 + scroll))
    screen.blit(bg_image, (0, -600 + scroll))

class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        
    def move(self):
        global game_over
        
        # Reset variables
        dx = 0
        dy = 0
        
        # Process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            game_over = True
            return

        # Collision with platforms
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = -20

        # Collision with springs
        for spring in spring_group:
            if spring.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < spring.rect.centery and self.vel_y > 0:
                    self.rect.bottom = spring.rect.top
                    dy = 0
                    self.vel_y = -35  # higher jump when hitting the spring

        # Collision with birds
        for bird in bird_group:
            if bird.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                game_over = True
                return

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Wrap around the screen horizontally
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0

        # Move player to bottom if they hit the top and generate new platforms below
        if self.rect.top <= 0:
            generate_new_platforms_below()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = bird_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_speed = 0.1
        self.animation_counter = 0
        self.vel_x = random.choice([-3, 3])
        self.vel_y = random.choice([-1, 1])
    
    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
        # Animate bird
        self.animation_counter += self.animation_speed
        if self.animation_counter >= len(self.frames):
            self.animation_counter = 0
        self.frame_index = int(self.animation_counter)
        self.image = self.frames[self.frame_index]

        # Move bird
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Wrap around screen
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vel_y *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, move_x=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = move_x
        self.original_x = x
         # 1 in 6 chance of having horizontal movement
        if random.randint(1, 6) == 1:
            self.move_x = random.choice([-2, 2])  # Random horizontal movement speed (-2 or 2)
        else:
            self.move_x = 0
        
        self.original_x = x 
        
    def update(self, scroll):
        self.rect.y += scroll
        self.rect.x += self.move_x

        # Reset platform position if it moves off-screen horizontally
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        # Check if the platform goes off the screen vertically
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spring_image, (30, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def create_platforms():
    platform_group.empty()
    y = SCREEN_HEIGHT - 40
    while y > -2000:
        x = random.randint(0, SCREEN_WIDTH - 60)
        width = random.randint(40, 60)
        move_x = random.choice([-2, 0, 2])  # Random horizontal movement speed (-2, 0, or 2)
        plat = Platform(x, y, width, move_x)
        platform_group.add(plat)
        y -= random.randint(80, 120)

def create_birds():
    bird_group.empty()
    for _ in range(2):  # Reduced number of birds from 5 to 2
        b_x = random.randint(0, SCREEN_WIDTH - BIRD_WIDTH)
        b_y = random.randint(-400, -200)
        bird = Bird(b_x, b_y)
        bird_group.add(bird)

def generate_new_platforms_below():
    for _ in range(5):
        x = random.randint(0, SCREEN_WIDTH - 60)
        y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 120)
        width = random.randint(40, 60)
        plat = Platform(x, y, width)
        platform_group.add(plat)
        if random.randint(1, 5) == 1:  # 20% chance to place a spring
            spring = Spring(x + random.randint(0, width - 30), y - 10)
            spring_group.add(spring)

def reset_game():
    global jumpy, platform_group, spring_group, bird_group, score, bg_scroll, game_over
    jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
    create_platforms()
    create_birds()
    
    # Add initial platform directly beneath the player
    initial_platform = Platform(jumpy.rect.centerx - 30, jumpy.rect.bottom + 10, 60)
    platform_group.add(initial_platform)
    
    score = 0
    bg_scroll = 0
    game_over = False

# Initialize player
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# Create sprite groups
platform_group = pygame.sprite.Group()
spring_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

# Create initial platforms and birds
create_platforms()
create_birds()

score = 0
game_over = False

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_bg(bg_scroll)
    
    # Update and draw platforms
    platform_group.update(bg_scroll)
    platform_group.draw(screen)
    
    # Update and draw springs
    spring_group.update(bg_scroll)
    spring_group.draw(screen)
    
    # Update and draw birds
    bird_group.update(bg_scroll)
    bird_group.draw(screen)
    
    if not game_over:
        jumpy.draw()
        jumpy.move()
        
        # Scroll the platforms down if the player reaches the scroll threshold
        if jumpy.rect.top <= SCROLL_THRESH:
            if jumpy.vel_y < 0:
                bg_scroll = abs(jumpy.vel_y)
                score += 1
            else:
                bg_scroll = 0
        else:
            bg_scroll = 0

        # Generate new platforms if needed
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = random.randint(-60, -30)
            move_x = random.choice([-2, 0, 2])  # Random movement speed
            plat = Platform(p_x, p_y, p_w, move_x)
            platform_group.add(plat)

        # Generate new birds if needed
        if len(bird_group) < 2:  # Reduced number of birds from 5 to 2
            b_x = random.randint(0, SCREEN_WIDTH - BIRD_WIDTH)
            b_y = random.randint(-400, -200)
            bird = Bird(b_x, b_y)
            bird_group.add(bird)

        # Check for game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        game_over_text = pygame.font.SysFont('Arial', 40).render('Game Over', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = pygame.font.SysFont('Arial', 20).render('Press R to Restart', True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))
    
    # Display score
    score_text = pygame.font.SysFont('Arial', 20).render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                reset_game()
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
