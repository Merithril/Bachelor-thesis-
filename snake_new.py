import pygame
import random

# set_up
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

# snake_1
snake1_head = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
snake1_body = [snake1_head.copy()]
snake1_length = 7

# snake_2
snake2_head = pygame.Vector2(100, 100)
snake2_body = [snake2_head.copy()]
snake2_length = 6

#snake score system
snake1_food = 0
snake2_food = 0
Goal = 3
game_over = False

# food
food_pos = pygame.Vector2(400, 200)
food_eaten = False
food_respawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # snake_1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: snake1_head.y -= 300 * dt
    if keys[pygame.K_s]: snake1_head.y += 300 * dt
    if keys[pygame.K_a]: snake1_head.x -= 300 * dt
    if keys[pygame.K_d]: snake1_head.x += 300 * dt

    # Snake1 Body
    snake1_body.insert(0, snake1_head.copy())
    if len(snake1_body) > snake1_length:
        snake1_body.pop()

    # sneak_2
    to_food = food_pos - snake2_head
    distance = to_food.length()
    if distance > 0:
        direction = to_food.normalize()
        snake2_head += direction * 150 * dt + pygame.Vector2(
            random.uniform(-50, 50) * dt,
            random.uniform(-50, 50) * dt
        )

    # Snake2 Body
    snake2_body.insert(0, snake2_head.copy())
    if len(snake2_body) > snake2_length:
        snake2_body.pop()

    # everything surrounding food
    # they can steal food
    snake1_eats = snake1_head.distance_to(food_pos) < 40 and not food_eaten
    snake2_eats = snake2_head.distance_to(food_pos) < 35 and not food_eaten

    if snake1_eats:
        snake1_length += 5
        snake1_food += 1  # ← NEU
        food_eaten = True
        print("snake_1 scores Score:", snake1_food)
    elif snake2_eats:
        snake2_length += 4
        snake2_food += 1  # ← NEU
        food_eaten = True
        print("snake_2 scores Score:", snake2_food)

        food_eaten = True
        print("snake_1 won length:", snake1_length)


    # food spawn
    if food_eaten:
        food_respawn_timer += dt
        if food_respawn_timer > 2.0:
            food_pos = pygame.Vector2(
                random.randint(50, 750),
                random.randint(50, 550)
            )
            food_eaten = False
            food_respawn_timer = 0


    screen.fill("black")

    # food implementation
    if not food_eaten:
        for dx in range(-12, 13, 4):
            for dy in range(-12, 13, 4):
                alpha = 255 - abs(dx) * 10 - abs(dy) * 10
                color = (255, 100 + alpha // 3, 100)
                pygame.draw.circle(screen, color,
                                   (int(food_pos.x + dx), int(food_pos.y + dy)), 8)

    # snake_1
    for i, segment in enumerate(snake1_body):
        color = (150, 50, 255) if i == 0 else (80, 80, 150)
        size = max(6, 22 - i * 2)
        pygame.draw.circle(screen, color, (int(segment.x), int(segment.y)), size)

    # snake_2
    for i, segment in enumerate(snake2_body):
        color = (255, 80, 80) if i == 0 else (200, 100, 100)
        size = max(5, 20 - i * 2)
        pygame.draw.circle(screen, color, (int(segment.x), int(segment.y)), size)

    # Score
    font = pygame.font.SysFont("Arial", 24)
    text1 = font.render(f"snake_1 : {snake1_length}", True, (150, 150, 255))
    text2 = font.render(f"snake_2: {snake2_length}", True, (255, 150, 150))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))

    # close
    esc_text = font.render("ESC beenden", True, (200, 200, 200))
    screen.blit(esc_text, (10, 570))

    pygame.display.flip()
    # === GAME OVER CHECK ===
    if snake1_food >= Goal and not game_over:
        game_over = True
        winner = "BLAU"
    elif snake2_food >= Goal and not game_over:
        game_over = True
        winner = "ROT"

    # VICTORY SCREEN (Spiel PAUSIERT)
    if game_over:
        # Screen abdunkeln
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((50, 0, 0))
        screen.blit(overlay, (0, 0))

        #dispay winner
        big_font = pygame.font.SysFont("Arial", 72, bold=True)
        win_text = big_font.render(f"🔥 {winner} won! 🔥", True, (255, 255, 0))
        win_rect = win_text.get_rect(center=(400, 250))
        screen.blit(win_text, win_rect)

        # Final Score
        score_font = pygame.font.SysFont("Arial", 36, bold=True)
        final_score = score_font.render(f"Final: 🔵{snake1_food}/10  🔴{snake2_food}/10", True, (255, 255, 255))
        screen.blit(final_score, (250, 320))

        # control
        restart_text = pygame.font.SysFont("Arial", 28).render("R = restart the game |  ESC = quit", True, (200, 200, 200))
        screen.blit(restart_text, (250, 400))
        continue

    # Live Score
    live_score = font.render(f"snake_1 {snake1_food}/10 vs snake_2 {snake2_food}/10", True, (255, 255, 255))
    screen.blit(live_score, (10, 70))

    dt = clock.tick(60) / 1000


if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_r and (snake1_food >= Goal or snake2_food >= Goal):
        # Reset Game
        snake1_head = pygame.Vector2(400, 300)
        snake1_body = [snake1_head.copy()]
        snake1_length = 7
        snake1_food = 0
        snake2_head = pygame.Vector2(100, 100)
        snake2_body = [snake2_head.copy()]
        snake2_length = 6
        snake2_food = 0
        food_pos = pygame.Vector2(400, 200)
        food_eaten = False

pygame.quit()
