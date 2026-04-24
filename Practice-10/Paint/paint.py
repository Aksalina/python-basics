import pygame

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

#pen
color = BLACK
tool = "pen"  

drawing = False
start_pos = None

radius = 5


#управление
running = True
screen.fill(WHITE)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ----------------- KEYBOARD -----------------
        if event.type == pygame.KEYDOWN:

            # инструменты: 1-кисть 2- прямоугольник 3 - круг 4 - ластик
            if event.key == pygame.K_1:
                tool = "pen"
            if event.key == pygame.K_2:
                tool = "rect"
            if event.key == pygame.K_3:
                tool = "circle"
            if event.key == pygame.K_4:
                tool = "eraser"

            # цвета 
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_k:
                color = BLACK

            # с - очистка
            if event.key == pygame.K_c:
                screen.fill(WHITE)

        # мышка 
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
                radius_c = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_c, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pen":
                pygame.draw.circle(screen, color, event.pos, radius)

            if drawing and tool == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 15)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()