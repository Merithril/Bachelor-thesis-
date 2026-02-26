
#import
import pygame

#initial setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

#Implement snake head
snake_head = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
snake_body = [snake_head.copy()]

#add food for snake
food_pos = pygame.Vector2(400, 200)
food_eaten = False
snake_length = 7


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake_head.y -= 300 * dt
    if keys[pygame.K_s]:
        snake_head.y += 300 * dt
    if keys[pygame.K_a]:
        snake_head.x -= 300 * dt
    if keys[pygame.K_d]:
        snake_head.x += 300 * dt

    # snakes growing with food
    if snake_head.distance_to(food_pos) < 40 and not food_eaten:
        snake_length += 5
        food_eaten = True
        print("EATEN! Länge:", snake_length)

    # body update
    if len(snake_body) > snake_length:
        snake_body.pop()
    snake_body.insert(0, snake_head.copy())

    # new food
    if food_eaten and snake_head.distance_to(food_pos) > 100:
        food_pos = pygame.Vector2(400, 300)
        food_eaten = False

    # RENDER
    screen.fill("black")
    for dx in range(-10, 11, 5):
        for dy in range(-10, 11, 5):
            pygame.draw.circle(screen, "purple", food_pos + pygame.Vector2(dx, dy), 6)

    for i, segment in enumerate(snake_body):
        color = "purple" if i == 0 else "gray"
        pygame.draw.circle(screen, color, (int(segment.x), int(segment.y)), max(5, 20 - i * 2))

    pygame.display.flip()
    dt = clock.tick(60) / 1000
