import pygame
import os
import sys
import win32com.client
import random
import time

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
window_title = "Snake"
icon_path = r"C:\python\snakegame\icon.ico"  # Replace with the path to your .ico file
script_to_run = os.path.abspath(__file__)

# Create or update the shortcut with the icon
create_or_update_shortcut(window_title, icon_path)

snake_speed = 15

# Window size
window_x = 800
window_y = 600

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialise game window
pygame.display.set_caption('Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Initial game state
def reset_game():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [100, 50]
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

reset_game()

# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_x / 10, 15)
    else:
        score_rect.midtop = (window_x / 2, window_y / 1.25)
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(1)

# Main Function
running = True
in_game = True
while running:
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    running = False
                    in_game = False

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        snake_position[1] -= 10 if direction == 'UP' else 0
        snake_position[1] += 10 if direction == 'DOWN' else 0
        snake_position[0] -= 10 if direction == 'LEFT' else 0
        snake_position[0] += 10 if direction == 'RIGHT' else 0

        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if (snake_position[0] < 0 or snake_position[0] > window_x - 10 or
                snake_position[1] < 0 or snake_position[1] > window_y - 10):
            game_over()
            in_game = False

        for block in snake_body[1:]:
            if snake_position == block:
                game_over()
                in_game = False

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                in_game = True
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
sys.exit()
