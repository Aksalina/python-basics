import pygame
from color_palette import *
import random

pygame.init()

#дисплей
WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 36)

# Game Over 
image_game_over = font.render("Game Over", True, colorRED)
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))


#GRID
def draw_grid():
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# змея
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1
        self.alive = True

    # движение змейки
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # ударение о стены
        head = self.body[0]

        if head.x < 0 or head.x >= WIDTH // CELL:
            self.alive = False

        if head.y < 0 or head.y >= HEIGHT // CELL:
            self.alive = False

    # рисование змейки
    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # проверка еды
    def check_collision(self, food):
        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            self.score += 1

            # змейка растёт
            self.body.append(Point(head.x, head.y))

            # новая еда
            food.generate_random_pos(self.body)

            # уровень
            self.level = 1 + self.score // 3

#появление еды
class Food:
    def __init__(self):
        self.pos = Point(5, 5)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    # еда не должна появляться на змейке
    def generate_random_pos(self, snake_body):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)

            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body):
                break


# init
clock = pygame.time.Clock()

snake = Snake()
food = Food()
food.generate_random_pos(snake.body)

FPS = 5
running = True


# loop
while running:
    screen.fill(colorBLACK)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #движение
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1

    
    if snake.alive:
        snake.move()
        snake.check_collision(food)

        draw_grid()
        snake.draw()
        food.draw()

        
        score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
        level_text = font.render(f"Level: {snake.level}", True, colorWHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (150, 10))

       
        clock.tick(FPS + snake.level)

    else:
        # окончание игры
        screen.fill(colorBLACK)
        screen.blit(image_game_over, image_game_over_rect)

        final_text = font.render(
            f"Score: {snake.score}  Level: {snake.level}",
            True,
            colorRED
        )
        screen.blit(final_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()

pygame.quit()