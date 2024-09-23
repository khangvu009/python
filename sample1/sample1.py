import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame")

# Load player image
player_image = pygame.image.load("C:\\python\\sample1\\player.png")
player_x, player_y = 100, 300

# Load enemy image
enemy_image = pygame.image.load("C:\\python\\sample1\\enemy.jpg")
enemy_x,enemy_y = 800, 300

# Initialize sound
pygame.mixer.init()
sound_effect = pygame.mixer.Sound("C:\\python\\sample1\\keysound.wav")
sound_effect_kill = pygame.mixer.Sound("C:\\python\\sample1\\killsound.mp3")

# Game loop (update)
running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
    # Play sound on user input
    # if event.type == pygame.KEYDOWN:
        # if event.key == pygame.K_SPACE:
            # sound_effect.play()


    # Update player position
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        sound_effect.play()
        player_x -= 1
    if keys[pygame.K_d]:
        sound_effect.play()
        player_x += 1
    if keys[pygame.K_w]:
        sound_effect.play()
        player_y -= 1
    if keys[pygame.K_s]:
        sound_effect.play()
        player_y += 1
        
     # Clear the screen
    screen.fill((0, 0, 0))

    # Draw player
    screen.blit(player_image, (player_x, player_y))
    
    # Draw enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))
    
    pygame.display.flip()
    
    if keys[pygame.K_a] and player_x < 0:
        player_x = 5
        sound_effect_kill.play()
    if keys[pygame.K_d] and player_x > width - player_image.get_width():
        player_x -= 5
        sound_effect_kill.play()
    if keys[pygame.K_w] and player_y < 0:
        player_y += 5
        sound_effect_kill.play()
    if keys[pygame.K_s] and player_y > height - player_image.get_height():
        player_y -= 5
        sound_effect_kill.play()
        
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw player
    screen.blit(player_image, (player_x, player_y))
    
    # Draw enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))
    
    pygame.display.flip()
    

pygame.quit()