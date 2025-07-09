import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Player setup
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)
player_speed = 5

# Bullet list
bullets = []

# Enemy list
enemies = []
enemy_spawn_timer = 0

# Score
score = 0

def spawn_enemy():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(0, HEIGHT - 30)
    while player.collidepoint(x, y):  # Prevent spawning on player
        x = random.randint(0, WIDTH - 30)
        y = random.randint(0, HEIGHT - 30)
    enemies.append(pygame.Rect(x, y, 30, 30))

def draw():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, player)

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Main game loop
running = True
while running:
    clock.tick(60)
    enemy_spawn_timer += 1

    if enemy_spawn_timer > 60:  # Spawn enemy every second
        spawn_enemy()
        enemy_spawn_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += player_speed
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += player_speed

    # Shooting input
    if keys[pygame.K_UP]:
        bullets.append(pygame.Rect(player.centerx - 5, player.top - 10, 10, 10))
    if keys[pygame.K_DOWN]:
        bullets.append(pygame.Rect(player.centerx - 5, player.bottom, 10, 10))
    if keys[pygame.K_LEFT]:
        bullets.append(pygame.Rect(player.left - 10, player.centery - 5, 10, 10))
    if keys[pygame.K_RIGHT]:
        bullets.append(pygame.Rect(player.right, player.centery - 5, 10, 10))

    # Move bullets
    for bullet in bullets[:]:
        if bullet.top < 0:
            bullet.y -= 10
        elif bullet.bottom > HEIGHT:
            bullet.y += 10
        elif bullet.left < 0:
            bullet.x -= 10
        elif bullet.right > WIDTH:
            bullet.x += 10

        # Remove off-screen bullets
        if (bullet.right < 0 or bullet.left > WIDTH or bullet.bottom < 0 or bullet.top > HEIGHT):
            bullets.remove(bullet)

    # Enemy movement towards player
    for enemy in enemies:
        if player.x > enemy.x:
            enemy.x += 2
        elif player.x < enemy.x:
            enemy.x -= 2
        if player.y > enemy.y:
            enemy.y += 2
        elif player.y < enemy.y:
            enemy.y -= 2

    # Collision detection (bullet vs enemy)
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # Collision detection (enemy vs player)
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over = font.render("GAME OVER", True, RED)
            screen.blit(game_over, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

    draw()
 