import pygame
import random

#SNAKE GAME

pygame.init()
WIDTH, HEIGHT = 600, 600
BLOCK = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Snake Game")
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


snake = [[100, 100], [80, 100], [60, 100], [40, 100]]
direction = 'RIGHT'
score = 0
lives = 3

def new_fruit():
    return [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]

fruit = new_fruit()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    head = snake[0].copy()
    if direction == 'UP':
        head[1] -= BLOCK
    elif direction == 'DOWN':
        head[1] += BLOCK
    elif direction == 'LEFT':
        head[0] -= BLOCK
    elif direction == 'RIGHT':
        head[0] += BLOCK

    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        lives -= 1
        if lives == 0:
            print("Game Over! Your score:", score)
            running = False
            continue
        snake = [[100, 100], [80, 100], [60, 100], [40, 100]]
        direction = 'RIGHT'
        continue
    if head == fruit:
        score += 1
        fruit = new_fruit()
    else:
        snake.pop()

    if head in snake:
        lives -= 1
        if lives == 0:
            print("Game Over! Your score:", score)
            running = False
            continue
        snake = [[100, 100], [80, 100], [60, 100], [40, 100]]
        direction = 'RIGHT'
        continue

    snake.insert(0, head)

    screen.fill(BLACK)
    for part in snake:
        pygame.draw.rect(screen, GREEN, (*part, BLOCK, BLOCK))
    pygame.draw.rect(screen, RED, (*fruit, BLOCK, BLOCK))
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
