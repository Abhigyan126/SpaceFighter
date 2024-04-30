import pygame
import random
import math

# Initialize Pygame
pygame.init()
score = 0

# Set the screen dimensions
WIDTH = 800
HEIGHT = 600

# Set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Set the clock for the game
clock = pygame.time.Clock()

# Load the spaceship image
spaceship_img = pygame.image.load("asset/spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (64, 64))

# Load the enemy spaceship image
enemy_img = pygame.image.load("asset/enemy_spaceship.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

# Load the power-up image
powerup_img = pygame.image.load("asset/powerup.png")
powerup_img = pygame.transform.scale(powerup_img, (32, 32))

# Load the space background image
background_img = pygame.image.load("asset/space_background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Set the player position
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 100

# Set the player speed
player_speed = 5

# Create a list to store the bullets
bullets = []

# Set the bullet properties
bullet_width = 4
bullet_height = 12
bullet_speed = 10

# Set the enemy properties
enemy_width = 64
enemy_height = 64
enemy_spawn_delay = 60

# Create a list to store the enemies
enemies = []

# Set the enemy types and their corresponding health values
enemy_types = [
    {"image": enemy_img, "speed": 3, "health": 1},
    {"image": enemy_img, "speed": 4, "health": 2},
    {"image": enemy_img, "speed": 5, "health": 3},
]

# Set the power-up properties
powerup_width = 32
powerup_height = 32
powerup_speed = 2
powerup_duration = 5
powerup_spawn_delay = 120

# Create a list to store the power-ups
powerups = []

# Set the score variable
# score = 0

# Set the power-up status variables
powerup_active = False
powerup_timer = 0

# Function to draw the player spaceship
def draw_player():
    screen.blit(spaceship_img, (player_x, player_y))

# Function to draw the enemies
def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy["image"], (enemy["x"], enemy["y"]))

# Function to draw the bullets
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_width, bullet_height))

# Function to draw the power-ups
def draw_powerups():
    for powerup in powerups:
        screen.blit(powerup_img, (powerup["x"], powerup["y"]))

# Function to move the bullets
def move_bullets(score):
    global powerup_active
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if powerup_active:
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
                if bullet_rect.colliderect(enemy_rect):
                    enemy["health"] -= 1
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        score += 1
        else:
            if bullet[1] < 0:
                bullets.remove(bullet)

# Function to move the enemies
def move_enemies():
    for enemy in enemies:
        enemy["y"] += enemy["speed"]

# Function to move the power-ups
def move_powerups():
    for powerup in powerups:
        powerup["y"] += powerup_speed

# Function to check bullet-enemy collisions
def check_bullet_enemy_collisions():
    global score
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemy["health"] -= 1
                if enemy["health"] <= 0:
                    enemies.remove(enemy)
                    score += 1
                return True
    return False

# Function to check player-enemy collisions
def check_player_enemy_collisions():
    player_rect = pygame.Rect(player_x, player_y, 64, 64)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Function to check player-powerup collisions
def check_player_powerup_collisions():
    global powerup_active, powerup_timer
    player_rect = pygame.Rect(player_x, player_y, 64, 64)
    for powerup in powerups[:]:
        powerup_rect = pygame.Rect(powerup["x"], powerup["y"], powerup_width, powerup_height)
        if player_rect.colliderect(powerup_rect):
            powerups.remove(powerup)
            powerup_active = True
            powerup_timer = powerup_duration * 60

# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet_x = player_x + 30
                bullet_y = player_y - bullet_height
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_x - bullet_x, bullet_y - mouse_y)
                bullet_dx = bullet_speed * math.sin(angle)
                bullet_dy = -bullet_speed * math.cos(angle)
                bullets.append([bullet_x, bullet_y, bullet_dx, bullet_dy])

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Update the player boundaries
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - 64:
        player_x = WIDTH - 64

    # Move the bullets
    move_bullets(score)

    # Update the enemy position and spawn new enemies
    if enemy_spawn_delay <= 0:
        enemy_type = random.choice(enemy_types)
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemies.append(
            {
                "image": enemy_type["image"],
                "x": enemy_x,
                "y": -enemy_height,
                "speed": enemy_type["speed"],
                "health": enemy_type["health"],
            }
        )
        enemy_spawn_delay = random.randint(60, 120)
    else:
        enemy_spawn_delay -= 1

    # Move the enemies
    move_enemies()

    # Update the power-up position and spawn new power-ups
    if powerup_spawn_delay <= 0:
        powerup_x = random.randint(0, WIDTH - powerup_width)
        powerups.append({"x": powerup_x, "y": -powerup_height})
        powerup_spawn_delay = random.randint(240, 480)
    else:
        powerup_spawn_delay -= 1

    # Move the power-ups
    move_powerups()

    # Check for bullet-enemy collisions
    check_bullet_enemy_collisions()

    # Check for player-enemy collisions
    if check_player_enemy_collisions():
        running = False

    # Check for player-powerup collisions
    check_player_powerup_collisions()

    # Draw the space background
    screen.blit(background_img, (0, 0))

    # Draw the player
    draw_player()

    # Draw the enemies
    draw_enemies()

    # Draw the bullets
    draw_bullets()

    # Draw the power-ups
    draw_powerups()

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
