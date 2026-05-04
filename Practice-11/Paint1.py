import pygame
import math

pygame.init()

# дисплей
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# текущий цвет и инструмент
color = BLACK
tool = "pen"

drawing = False
start_pos = None

radius = 5

running = True
screen.fill(WHITE)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        #Обозначения
        if event.type == pygame.KEYDOWN:

            # инструменты
            if event.key == pygame.K_1:
                tool = "pen"
            if event.key == pygame.K_2:
                tool = "rect"
            if event.key == pygame.K_3:
                tool = "circle"
            if event.key == pygame.K_4:
                tool = "eraser"
            if event.key == pygame.K_5:
                tool = "square"
            if event.key == pygame.K_6:
                tool = "r_triangle"
            if event.key == pygame.K_7:
                tool = "eq_triangle"
            if event.key == pygame.K_8:
                tool = "rhombus"

            # цвета
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_k:
                color = BLACK

            # очистка
            if event.key == pygame.K_c:
                screen.fill(WHITE)

        # нажатие пкм
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

    
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # прямоугольник
            if tool == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(screen, color, (x, y, w, h), 2)

            # круг
            if tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, r, 2)

            #квадрат
            if tool == "square":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                size = min(abs(dx), abs(dy))  # одинаковые стороны

                x = start_pos[0]
                y = start_pos[1]

                if dx < 0:
                    x -= size
                if dy < 0:
                    y -= size

                pygame.draw.rect(screen, color, (x, y, size, size), 2)

            # р треугольник
            if tool == "r_triangle":
                p1 = start_pos
                p2 = (start_pos[0], end_pos[1])
                p3 = (end_pos[0], end_pos[1])
                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            # равносторонний треугольник
            if tool == "eq_triangle":
                dx = end_pos[0] - start_pos[0]
                side = abs(dx)

                height = int((math.sqrt(3) / 2) * side)

                if dx >= 0:
                    p1 = start_pos
                    p2 = (start_pos[0] + side, start_pos[1])
                    p3 = (start_pos[0] + side // 2, start_pos[1] - height)
                else:
                    p1 = start_pos
                    p2 = (start_pos[0] - side, start_pos[1])
                    p3 = (start_pos[0] - side // 2, start_pos[1] - height)

                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            # ромб
            if tool == "rhombus":
                cx = (start_pos[0] + end_pos[0]) // 2
                cy = (start_pos[1] + end_pos[1]) // 2

                dx = abs(end_pos[0] - start_pos[0]) // 2
                dy = abs(end_pos[1] - start_pos[1]) // 2

                p1 = (cx, cy - dy)
                p2 = (cx + dx, cy)
                p3 = (cx, cy + dy)
                p4 = (cx - dx, cy)

                pygame.draw.polygon(screen, color, [p1, p2, p3, p4], 2)

        # рисование
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pen":
                pygame.draw.circle(screen, color, event.pos, radius)

            if drawing and tool == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 15)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()